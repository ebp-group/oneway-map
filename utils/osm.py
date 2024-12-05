import osmapi
from pprint import pprint


def get_changeset_info(changeset):
  api = osmapi.OsmApi()
  try:
      return api.ChangesetGet(changeset)
  except osmapi.ApiError as e:
      print(f"Error: {e}")
      return None
