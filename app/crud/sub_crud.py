from app.database import db_dependency
from app.schemas.sub_schemas import SubscriptionBase, SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from app.models import Subscriptions
from typing import List

class SubscriptionCrud:
    """ This class will contain the CRUD functions for Subscriptions """
    
    def create_new_subscriptions(self, sub: SubscriptionCreate, db: db_dependency) -> Subscriptions:
        """ Creates a new subscription in the database.

        Args:
            sub (SubscriptionCreate): The subscription data.

        Returns:
            Subscriptions: The created subscription instance.

        Raises:
            ValueError: If the provided data is invalid.
        """
        self._validate_create_data(sub)

        new_subscription = Subscriptions(
            service_name=sub.service_name, 
            monthly_cost=sub.monthly_cost, 
            renewal_date=sub.renewal_date,
            user_id=sub.user_id  # Foreign Key
        )
        
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        
        return new_subscription

    def update_subscription(self, sub_id: int, sub: SubscriptionUpdate, db: db_dependency) -> Subscriptions:
        """ Updates a subscription in the database.

        Args:
            sub_id (int): The ID of the subscription to update.
            sub (SubscriptionUpdate): The updated data.

        Returns:
            Subscriptions: The updated subscription instance.

        Raises:
            ValueError: If the subscription does not exist or data is invalid.
        """
        existing_subscription = self.get_subscription_by_id(sub_id, db)
        if not existing_subscription:
            raise ValueError('Subscription not found')

        self._apply_updates(existing_subscription, sub)

        try:
            db.commit()
            return existing_subscription
        except Exception as e:
            db.rollback()
            raise Exception("Failed to update subscription") from e

    # Having '_' at the start of the function name lets developers know its for internal use in the OOP.
    def _validate_create_data(self, sub: SubscriptionCreate):
        """ Validates the input data for creating a new subscription. """
        if not sub.service_name or len(sub.service_name) == 0:
            raise ValueError('Service name is required')
        if sub.monthly_cost <= 0:
            raise ValueError('Monthly cost must be a positive number')
        # Can add more validations as needed
        
    def get_all_subscriptions(self, db: db_dependency) -> List[Subscriptions]:
        """ Retrieves all subscriptions from the database. """
        return db.query(Subscriptions).all()

    def get_subscription_by_id(self, sub_id: int, db: db_dependency) -> Subscriptions:
        """ Returns a subscription by its ID. """
        return db.query(Subscriptions).filter(Subscriptions.id == sub_id).first()
    
    def subscriptions_per_user(self, user_id: int, db: db_dependency) -> Subscriptions:
        """ Returns subscriptions per user. """
        return db.query(Subscriptions).filter(Subscriptions.user_id == user_id).all()

    def _apply_updates(self, existing_subscription: Subscriptions, sub_update: SubscriptionUpdate):
        """ Applies updates from the SubscriptionUpdate to an existing subscription. """
        if sub_update.service_name is not None:
            existing_subscription.service_name = sub_update.service_name
        if sub_update.monthly_cost is not None:
            existing_subscription.monthly_cost = sub_update.monthly_cost
        if sub_update.renewal_date is not None:
            existing_subscription.renewal_date = sub_update.renewal_date
        
    def delete_subscription(self,sub_id: int, db: db_dependency):
        """ Deletes a subscription by its ID. """
        existing_subscription = self.get_subscription_by_id(sub_id, db)
        if not existing_subscription:
            raise ValueError('Subscription not found')
        try:
            db.delete(existing_subscription)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise Exception("Failed to delete subscription") from e
        