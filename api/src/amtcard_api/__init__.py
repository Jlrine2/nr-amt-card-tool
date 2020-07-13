import connexion
import boto3

connexion_app = connexion.App(__name__)

from amtcard_api import handlers  # noqa Has to be at end of file or will cause circular import

__all__ = ['handlers', 'connexion_app']
