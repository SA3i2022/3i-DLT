def data_generator(original_dir, mask_dir):
    original_files = original_dir
    mask_files = mask_dir
    original_files.sort()
    mask_files.sort()

    for original_file, mask_file in zip(original_files, mask_files):
        original_array = np.load(original_file)
        #original_array=np.expand_dims(original_array, axis= -1)
        mask_array = np.load(mask_file)

        yield original_array, mask_array
