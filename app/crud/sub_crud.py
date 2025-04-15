from app.database import db_dependency
from app.schemas.sub_schemas import SubscriptionBase, SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from app.models import Subscriptions

class SubscriptionCrud():
    """ This class will contain the CRUD functions for Subscriptions """
    
    def create_new_subscriptions(self, sub: SubscriptionCreate, db: db_dependency):
        """ This function will create a new subscription in the database """
        
        new_subscription = Subscriptions(
            service_name = sub.service_name, 
            monthly_cost = sub.monthly_cost, 
            renewal_date = sub.renewal_date,
            user_id = sub.user_id # Foreign Key
            )
        
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        
        return new_subscription
    
    def get_all_subscriptions(self, db: db_dependency):
        """ This function will return all subscriptions in the database """
        return db.query(Subscriptions).all()
    
    def subscriptions_per_user(self, user_id: int, db: db_dependency):
        """ This function will return all subscriptions for a specific user """
        return db.query(Subscriptions).filter(Subscriptions.user_id == user_id).all()
    
    def get_subscription_by_id(self, sub_id: int, db: db_dependency):
        """ This function will return a subscription by its id """
        return db.query(Subscriptions).filter(Subscriptions.id == sub_id).first()
    
    def update_subscription(self, sub_id: int, sub: SubscriptionUpdate, db: db_dependency):
        """ This function will update a subscription in the database """
        
        existing_subscription = db.query(Subscriptions).filter(Subscriptions.id == sub_id)
        
        if not existing_subscription:
            return ValueError('Subscription not found') # Continue this look back at senior Code on ChatAI
        
        
        