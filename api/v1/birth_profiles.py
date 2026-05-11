"""
Birth Profile endpoints — guarded by Supabase Auth and PostgreSQL RLS.

Every query runs under the seeker's own JWT, so the database itself
refuses to surrender records that do not belong to the caller.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import AuthContext, get_current_user
from core.supabase_client import get_user_supabase
from models.birth_profile import BirthProfile, BirthProfileCreate

router = APIRouter(prefix="/birth-profiles", tags=["birth-profiles"])

_TABLE = "birth_profiles"


@router.post("", response_model=BirthProfile, status_code=status.HTTP_201_CREATED)
def create_birth_profile(
    payload: BirthProfileCreate,
    auth: AuthContext = Depends(get_current_user),
) -> BirthProfile:
    """Seal a new ancestral record into the great wheel."""
    sb = get_user_supabase(auth.jwt_token)
    row = {
        "user_id": auth.user_id,
        "name": payload.name,
        "birth_datetime": payload.birth_datetime.isoformat(),
        "latitude": payload.latitude,
        "longitude": payload.longitude,
    }
    result = sb.table(_TABLE).insert(row).execute()
    if not result.data:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Insert failed.")
    return BirthProfile(**result.data[0])


@router.get("", response_model=list[BirthProfile])
def list_birth_profiles(
    auth: AuthContext = Depends(get_current_user),
) -> list[BirthProfile]:
    """List the seeker's own sky-maps. RLS filters out all others."""
    sb = get_user_supabase(auth.jwt_token)
    result = sb.table(_TABLE).select("*").order("created_at", desc=True).execute()
    return [BirthProfile(**row) for row in (result.data or [])]


@router.get("/{profile_id}", response_model=BirthProfile)
def get_birth_profile(
    profile_id: UUID,
    auth: AuthContext = Depends(get_current_user),
) -> BirthProfile:
    """Retrieve one ancestral record by id, if RLS permits."""
    sb = get_user_supabase(auth.jwt_token)
    result = sb.table(_TABLE).select("*").eq("id", str(profile_id)).limit(1).execute()
    if not result.data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Birth profile not found.")
    return BirthProfile(**result.data[0])


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_birth_profile(
    profile_id: UUID,
    auth: AuthContext = Depends(get_current_user),
) -> None:
    """Erase an ancestral record. RLS ensures only the owner may strike."""
    sb = get_user_supabase(auth.jwt_token)
    result = sb.table(_TABLE).delete().eq("id", str(profile_id)).execute()
    if not result.data:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Birth profile not found.")
    return None
