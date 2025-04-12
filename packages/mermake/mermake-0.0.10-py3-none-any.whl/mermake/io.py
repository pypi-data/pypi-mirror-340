import os
import gc
import glob

import zarr
from dask import array as da
import cupy as cp
import numpy as np

class DaskArrayWithMetadata:
	def __init__(self, dask_array, path):
		self.dask_array = dask_array
		self.path = path

	def __getattr__(self, attr):
		# This will forward any unknown attributes to the Dask array
		return getattr(self.dask_array, attr)

	def __repr__(self):
		return f"<DaskArrayWithMetadata(shape={self.dask_array.shape}, path={self.path})>"

def read_im(path,return_pos=False):
	dirname = os.path.dirname(path)
	fov = os.path.basename(path).split('_')[-1].split('.')[0]
	file_ = dirname+os.sep+fov+os.sep+'data'
	image = da.from_zarr(file_)[1:]

	shape = image.shape
	#nchannels = 4
	xml_file = os.path.dirname(path)+os.sep+os.path.basename(path).split('.')[0]+'.xml'
	if os.path.exists(xml_file):
		txt = open(xml_file,'r').read()
		tag = '<z_offsets type="string">'
		zstack = txt.split(tag)[-1].split('</')[0]
		
		tag = '<stage_position type="custom">'
		x,y = eval(txt.split(tag)[-1].split('</')[0])
		
		nchannels = int(zstack.split(':')[-1])
		nzs = (shape[0]//nchannels)*nchannels
		image = image[:nzs].reshape([shape[0]//nchannels,nchannels,shape[-2],shape[-1]])
		image = image.swapaxes(0,1)
		# this make the channel dimension the fastest changing so 'views' are produced from indexing
		#image = image.transpose(0, 2, 3, 1)  # shape = (zplanes, Y, X, nchannels)

	#image = DaskArrayWithMetadata(image, path)
	if return_pos:
		return image,x,y
	return image

class Container:
	def __init__(self, data, **kwargs):
		# Store the array and any additional metadata
		self.data = data
		self.metadata = kwargs
	def __getitem__(self, item):
		# Allow indexing into the container
		return self.data[item]
	def __array__(self):
		# Return the underlying array
		return self.data
	def __repr__(self):
		# Custom string representation showing the metadata or basic info
		return f"Container(shape={self.data.shape}, dtype={self.data.dtype}, metadata={self.metadata})"
	def __getattr__(self, name):
		# If attribute is not found on the container, delegate to the CuPy object
		if hasattr(self.data, name):
			return getattr(self.data, name)
		raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
	def clear(self):
		# Explicitly delete the CuPy array to release memory
		del self.data
		cp._default_memory_pool.free_all_blocks()
		cp._default_pinned_memory_pool.free_all_blocks()

def read_cim(path):
	im = read_im(path)
	cim = cp.asarray(im)
	container = Container(cim)
	container.path = path
	return container

def get_iH(fld): return int(os.path.basename(fld).split('_')[0][1:])
def get_files(master_data_folders, set_ifov,iHm=None,iHM=None):
	#if not os.path.exists(save_folder): os.makedirs(save_folder)
	all_flds = []
	for master_folder in master_data_folders:
		all_flds += glob.glob(master_folder+os.sep+r'H*_AER_*')
		#all_flds += glob.glob(master_folder+os.sep+r'H*_Igfbpl1_Aldh1l1_Ptbp1*')
	### reorder based on hybe
	all_flds = np.array(all_flds)[np.argsort([get_iH(fld)for fld in all_flds])] 
	set_,ifov = set_ifov
	all_flds = [fld for fld in all_flds if set_ in os.path.basename(fld)]
	all_flds = [fld for fld in all_flds if ((get_iH(fld)>=iHm) and (get_iH(fld)<=iHM))]
	#fovs_fl = save_folder+os.sep+'fovs__'+set_+'.npy'
	folder_map_fovs = all_flds[0]#[fld for fld in all_flds if 'low' not in os.path.basename(fld)][0]
	fls = glob.glob(folder_map_fovs+os.sep+'*.zarr')
	fovs = np.sort([os.path.basename(fl) for fl in fls])
	fov = fovs[ifov]
	all_flds = [fld for fld in all_flds if os.path.exists(fld+os.sep+fov)]
	return all_flds,fov


import concurrent.futures
def image_generator(hybs, fovs):
	"""Generator that prefetches the next image while processing the current one."""
	with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
		future = None  # Holds the future for the next image
		for all_flds, fov in zip(hybs, fovs):
			for hyb in all_flds:
				file = os.path.join(hyb, fov)

				# Submit the next image read operation
				next_future = executor.submit(read_cim, file)
				# If there was a previous future, yield its result
				if future:
					yield future.result()
				# Move to the next future
				future = next_future

		# Yield the last remaining image
		if future:
			yield future.result()

from pathlib import Path
def path_parts(path):
	path_obj = Path(path)
	fov = path_obj.stem  # The filename without extension
	tag = path_obj.parent.name  # The parent directory name (which you seem to want)
	return fov, tag

# Function to handle saving the file
def save_data(save_folder, path, icol, Xhf):
	fov,tag = path_parts(path)
	save_fl = save_folder + os.sep + fov + '--' + tag + '--col' + str(icol) + '__Xhfits.npz'
	os.makedirs(save_folder, exist_ok = True)
	cp.savez_compressed(save_fl, Xh=Xhf)
	del Xhf
def save_data_dapi(save_folder, path, icol, Xh_plus, Xh_minus):
	fov, tag = path_parts(path)
	save_fl = os.path.join(save_folder, f"{fov}--{tag}--col{icol}__Xhfits.npz")
	os.makedirs(save_folder, exist_ok=True)
	cp.savez_compressed(save_fl, Xh_plus=Xh_plus, Xh_minus=Xh_minus)
	del Xh_plus, Xh_minus


def profile():
	import gc
	mempool = cp.get_default_memory_pool()
	# Loop through all objects in the garbage collector
	for obj in gc.get_objects():
		if isinstance(obj, cp.ndarray):
			# Check if it's a view (not a direct memory allocation)
			if obj.base is not None:
				# Skip views as they do not allocate new memory
				continue
			print(f"CuPy array with shape {obj.shape} and dtype {obj.dtype}")
			print(f"Memory usage: {obj.nbytes / 1024**2:.2f} MB")  # Convert to MB
	print(f"Used memory after: {mempool.used_bytes() / 1024**2:.2f} MB")





