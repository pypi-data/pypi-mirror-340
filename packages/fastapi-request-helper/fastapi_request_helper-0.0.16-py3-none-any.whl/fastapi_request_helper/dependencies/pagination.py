from fastapi import Query


class PaginationParams:
<<<<<<< Updated upstream
    def __init__(
        self,
        page: int = Query(default=1, ge=1, le=10000),
        per_page: int = Query(default=10, ge=1, le=20),
    ):
        self.page = page
        self.per_page = per_page
=======
  def __init__(
    self,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
  ):
    self.page = page
    self.per_page = per_page
>>>>>>> Stashed changes
