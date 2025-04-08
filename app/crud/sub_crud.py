from app.database import db_dependency
from app.schemas.sub_schemas import SubscriptionBase, SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from models import Subscriptions

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