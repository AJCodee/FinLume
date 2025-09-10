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
    
    def update_category(self, category_id: int, category_data: CategoryUpdate, db: DbDep) -> Category:
        """ This method will update a category in the database. 
        
        Args:
            category_id (int) ID of the exsisting Category.
            category_data (CategoryUpdate): the updated data.
            
        Raises:
            ValueError: If the Category does not exist or the data is invalid.
            """
            
        exsisting_category = self.get_category_by_id(category_id, db)
        if not exsisting_category:
            raise ValueError("Category not found")
        
        self._apply_updates(exsisting_category, category_data) # Need to create _apply_updates.
        
        try:
            db.commit()
            return exsisting_category
        except Exception as e:
            db.rollback()
            raise ValueError("Failed to update category") from e 
        
    def get_all_categorys(self, db: DbDep):
        """ This method will return all the Categorys in the database. """
        return db.query(Category).all()