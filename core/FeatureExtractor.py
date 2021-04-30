from typing import List

import numpy as np
from sklearn.cluster import KMeans

from core.Spotify import Spotify

class FeatureExtractor:
  RANDOM_STATE = 42
  
  def __init__(self, client: Spotify, track_ids: List[str]):
    self.track_ids = track_ids
    self.client = client
    self.features = None
  
  def extract_raw_features(self, normalize: bool = False):
    """
    Extract raw features from a list of tracks provided. Currently using the Spotify's Echonest API.
    Stores the result in `features` data member of the this class.
    :param normalize: Normalize all features to have a range from 0 to 1. Better for application in ML algorithms later.
    :return:
    """
    self.features = self.client.get_audio_features(self.track_ids)
    
    if normalize:
      """
      Normalizes loudness (assumed range: 0 to -60) and tempo (assumed range: 50 to 200).
      Hard-max/Hard-min if values out of range.
      """
      for i, track in enumerate(self.features):
        x = track['loudness']
        x = max(min(x, 0), -60) / (-60)
        self.features[i]['loudness'] = round(x, 4)

        x = track['tempo']
        x = (max(min(x, 200), 50) - 50) / (200 - 50)
        self.features[i]['tempo'] = round(x, 4)
  
  def compute_clusters_in_tracks(self, features_list: List[str], n_clusters: int = 4) -> List[List[float]]:
    """
    Compute clusters from a list of tracks given. Uses KMeans algorithm.
    :param features_list: A list of names of features to be used.
    :param n_clusters: Number of clusters to compute.
    :return: A list of coordinates of cluster centers in n-dimensional space.
    """
    if self.features is None:
      self.extract_raw_features(normalize=True)

    # fixed random state for easy reproduction of bugs
    kmeans = KMeans(n_clusters=n_clusters, random_state=FeatureExtractor.RANDOM_STATE)
    vectors = [[track[feature] for feature in features_list] for track in self.features]
    kmeans.fit(vectors)
    
    return kmeans.cluster_centers_.tolist()
