"""
Comments API Router

Comment and mention endpoints (8+ endpoints).
"""

from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from domains.identity.dependencies import get_current_active_user
from domains.identity.models import User
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Comment
from .repository import CommentRepository
from .schemas import CommentCreate, CommentRead, CommentUpdate, ReactionAdd

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    data: CommentCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Create a comment."""
    repo = CommentRepository(db)
    
    # TODO: Parse markdown and generate HTML
    comment = Comment(
        **data.model_dump(),
        author_id=current_user.id,
        tenant_id=current_user.tenant_id,
        content_html=None,  # Would be generated from markdown
    )
    created = await repo.create(comment)
    await db.commit()
    await db.refresh(created)
    
    # TODO: Send notifications to mentioned users
    if created.mentions:
        pass  # Implement mention notifications
    
    return created


@router.get("", response_model=List[CommentRead])
async def list_comments(
    entity_type: str,
    entity_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """List comments for an entity."""
    repo = CommentRepository(db)
    comments = await repo.get_by_entity(entity_type, entity_id, skip, limit)
    return comments


@router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(
    comment_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get a comment by ID."""
    repo = CommentRepository(db)
    comment = await repo.get(comment_id)
    if not comment or comment.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.patch("/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: UUID,
    data: CommentUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Update a comment."""
    from datetime import datetime
    repo = CommentRepository(db)
    comment = await repo.get(comment_id)
    if not comment or comment.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
    
    comment.content = data.content
    comment.is_edited = True
    comment.edited_at = datetime.utcnow()
    
    updated = await repo.update(comment)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Delete a comment."""
    from datetime import datetime
    repo = CommentRepository(db)
    comment = await repo.get(comment_id)
    if not comment or comment.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    comment.is_deleted = True
    comment.deleted_at = datetime.utcnow()
    await repo.update(comment)
    await db.commit()


@router.get("/{comment_id}/replies", response_model=List[CommentRead])
async def get_comment_replies(
    comment_id: UUID,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """Get replies to a comment (threading)."""
    repo = CommentRepository(db)
    replies = await repo.get_replies(comment_id, skip, limit)
    return replies


@router.post("/{comment_id}/reactions", response_model=CommentRead)
async def add_reaction(
    comment_id: UUID,
    reaction: ReactionAdd,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Add a reaction (emoji) to a comment."""
    repo = CommentRepository(db)
    comment = await repo.get(comment_id)
    if not comment or comment.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Add or update reaction
    emoji = reaction.emoji
    if emoji not in comment.reactions:
        comment.reactions[emoji] = []
    
    user_id_str = str(current_user.id)
    if user_id_str not in comment.reactions[emoji]:
        comment.reactions[emoji].append(user_id_str)
    
    updated = await repo.update(comment)
    await db.commit()
    await db.refresh(updated)
    return updated


@router.delete("/{comment_id}/reactions/{emoji}", response_model=CommentRead)
async def remove_reaction(
    comment_id: UUID,
    emoji: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Remove a reaction from a comment."""
    repo = CommentRepository(db)
    comment = await repo.get(comment_id)
    if not comment or comment.tenant_id != current_user.tenant_id:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    user_id_str = str(current_user.id)
    if emoji in comment.reactions and user_id_str in comment.reactions[emoji]:
        comment.reactions[emoji].remove(user_id_str)
        if not comment.reactions[emoji]:
            del comment.reactions[emoji]
    
    updated = await repo.update(comment)
    await db.commit()
    await db.refresh(updated)
    return updated
