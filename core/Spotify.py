import requests
import base64
import os
import logging
from typing import Dict, List

logging.basicConfig(filename="Spotify.log")


class Spotify:
  BASE_URL = "https://api.spotify.com"
  AUDIO_FEATURES = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                    'instrumentalness', 'liveness', 'valence', 'tempo']
  logger = logging.getLogger("Spotify")
  
  class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str = None):
      self.status_code = status_code
      self.detail = detail
      super().__init__(f"HTTP {self.status_code}: {self.detail}")
  
  def __init__(self):
    self.client_id = os.getenv("SPOTIFY_CLIENT_ID", "client_id")
    self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "client_secret")
    
    self.access_token = self.__refresh_access_token()
  
  def __refresh_access_token(self) -> str:
    client_credentials = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode('ascii')).decode()
    res = requests.post(f"https://accounts.spotify.com/api/token",
                        headers={'Authorization': f"Basic {client_credentials}"},
                        data={'grant_type': 'client_credentials'})
    
    if res.status_code == requests.codes.BAD_REQUEST:
      Spotify.logger.error("Wrong (client_id, client_secret) combination. Could not refresh access token.")
      raise Spotify.HTTPException(requests.codes.BAD_REQUEST, detail="Something went wrong from our side.")
    
    return res.json()['access_token']
  
  def make_api_call(self, method: str, url: str, headers=None, data=None, **kwargs):
    if data is None:
      data = {}
    if headers is None:
      headers = {}
    
    res = requests.request(method, url, headers=headers, data=data, **kwargs)
    
    if res.status_code == requests.codes.ok:
      return res.json()
    
    if res.status_code == requests.codes.unauthorized:
      self.access_token = self.__refresh_access_token()
      return self.make_api_call(method, url, headers, data, **kwargs)
    
    detail = res.json()['error']['message']
    Spotify.logger.error(f"HTTP{res.status_code}: {method}, {url}: {detail}")
    raise Spotify.HTTPException(status_code=res.status_code, detail=detail)
  
  def get_audio_features(self, track_ids: List[str]) -> List[Dict]:
    res = self.make_api_call('get', url=f"{Spotify.BASE_URL}/v1/audio-features",
                             headers={
                               'Authorization': f'Bearer {self.access_token}',
                               'Accept': 'application/json',
                               'Content-Type': 'application/json'
                             },
                             params={'ids': ','.join(track_ids)})
    
    data = []
    
    for i, item in enumerate(res['audio_features']):
      if item is None:
        Spotify.logger.warning(f"spotify:track:{track_ids[i]} does not have audio features. Omitted.")
        continue
      track_features = {}
      for feature in Spotify.AUDIO_FEATURES:
        track_features[feature] = item[feature]
      
      data.append(track_features)
    
    return data
