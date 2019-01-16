from scipy.ndimage import label


DEFAULT_THRESHOLD = 0.2

def find_blobs(da, threshold=DEFAULT_THRESHOLD):
    print("Lookin for some blobs at threshold {} in da {}"
          .format(str(threshold), str(da)))
    return ['Some', 'blobs', 'I', 'found']
