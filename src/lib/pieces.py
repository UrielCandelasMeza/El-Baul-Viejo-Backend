from extensions import db
from src.models.piece_model import Piece, PieceStatus
from src.models.category_model import Category

def _get_available_pieces():
  """Gets all available pieces from the db"""
  pieces = db.session.execute(
      db.select(Piece).where(Piece.status == PieceStatus.AVAILABLE)
  ).scalars().all()

  return pieces


def _get_all_pieces():
  """Gets all pieces from the db"""
  pieces = db.session.execute(
      db.select(Piece)
  ).scalars().all()

  return pieces


def _get_one_piece(piece_id: str):
  """Get one piece from the db"""
  piece = db.session.get(Piece, piece_id)

  if not piece:
      return None

  return piece

def _search_by_name(query: str):
  pieces = db.session.execute(
      db.select(Piece).where(Piece.name.icontains(query)) # <--- Cambiado aquí
  ).scalars().all()
  return pieces

def _search_by_category(query: str):
  """
  Busca categorías que coincidan con el query,
  luego devuelve (piezas_con_esa_categoria, categorias_encontradas).
  """
  categories = db.session.execute(
    db.select(Category).where(Category.name.icontains(query))
  ).scalars().all()

  if not categories:
    return [], []

  category_ids_str = [str(c.id) for c in categories]

  # category_ids es un JSON array de strings → filtramos en Python
  all_pieces = db.session.execute(db.select(Piece)).scalars().all()
  matching = [
    p for p in all_pieces
    if any(cid in (p.category_ids or []) for cid in category_ids_str)
  ]

  return matching, list(categories)