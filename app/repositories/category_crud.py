# Crud for category.

from app.db.models import Category
from app.schemas.category_shemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.api.deps import DbDep

class CategoryCrud:
    """ This class will contain the CRUD operations for the Category model. """
    
    def create_new_category(self, user_id: int, category: CategoryCreate, db: DbDep) -> Category:
        """ This method will create and return a new category for the given user.
        
        Args: 
            category (Category: CategoryCreate) contains category data
            
        Returns:
            Category: The create Category instance.
            """
            
        new_category = Category(
            user_id = user_id,
            name = category.name
            )
        
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return(new_category)
        