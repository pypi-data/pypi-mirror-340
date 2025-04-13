import math

def compute_pagination(count, limit, offset):
    total_pages = math.ceil(count / limit) if limit else 1
    page_list = [
        {
            "page": page,
            "offset": (page - 1) * limit
        }
        for page in range(1, total_pages + 1)
    ]

    pagination = {
        "count": count,
        "total_pages": total_pages,
        "page_list": page_list,
        "offset": offset,
        "limit": limit,
        "current_page": (offset // limit) + 1 if limit else 1,
        "has_next": (offset + limit) < count,
        "has_prev": offset > 0,
    }

    return pagination
