"""ESI interactions"""

from corptools.task_helpers.corp_helpers import get_corp_token

from esi.clients import EsiClientProvider

from allianceauth.services.hooks import get_extension_logger

from . import __version__

logger = get_extension_logger(__name__)
esi = EsiClientProvider(app_info_text=f"aa-corp-handouts v{__version__}")


def get_corporation_asset_names(
    corporation_id: int, item_ids: list[int]
) -> list[[int, int]]:
    """
    Return names for a set of item ids, which you can get from corporation assets endpoint.
    """
    logger.info("Updating names for corp id %d", corporation_id)
    logger.debug(item_ids)

    req_scopes = ["esi-assets.read_corporation_assets.v1"]
    req_roles = ["Director"]
    token = get_corp_token(corporation_id, req_scopes, req_roles)

    return esi.client.Assets.post_corporations_corporation_id_assets_names(
        corporation_id=corporation_id,
        item_ids=item_ids,
        token=token.valid_access_token(),
    ).result()
