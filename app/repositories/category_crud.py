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
    
    def get_category_by_id(self, category_id: int, db: DbDep):
        """ This method will return a category by ID"""
        return db.query(Category).filter(Category.id == category_id).first()
    
    def _apply_updates(self, exsisting_category: Category, category_update: CategoryUpdate):
        """ This model will apply updates to the exsisting category """
        if category_update.name is not None:
            exsisting_category.name = category_update.name
            
    def delete_category(self, category_id: int, db: DbDep):
        """ This method will delete an exsisting category from the database """
        exsisting_category = self.get_category_by_id(category_id, db)
        if not exsisting_category:
            raise ValueError("Category does not exist")
        try:
            db.delete(exsisting_category)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise ValueError("Failed to delete category") from e 