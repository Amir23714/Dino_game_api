import datetime

from models.models import User as UserModel
from models.models import WorkingUsers as WorkingUserModel
from DTO.user import User as UserDTO

statuses = {1000: "junior developer", 5000: "middle developer", 10000: "senior developer"}


def create_user(data: UserDTO, db):
    user = UserModel(telegram_id=data.telegram_id, username=data.username, status=data.status,
                     experience=data.experience, isAdmin=data.isAdmin)

    try:
        db.add(user)
        db.commit()
    except Exception as e:
        print(e)

    return user


def get_user(telegram_id: str, db):
    return db.query(UserModel).filter(UserModel.telegram_id == telegram_id).first()


def change_status(telegram_id: str, status: str, db):
    user = get_user(telegram_id, db)
    user.status = status
    db.commit()
    db.refresh(user)


def get_user_work(telegram_id: str, db):
    user = db.query(WorkingUserModel).filter(WorkingUserModel.telegram_id == telegram_id).first()
    return user


def make_user_work(telegram_id: str, working_status: str, finish_time: int, db):
    user = get_user_work(telegram_id, db)

    if user is not None:
        print(123)
        return user, False

    user = WorkingUserModel(telegram_id=telegram_id, working_status=working_status, finish=finish_time)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user, True


def delete_user_work(telegram_id: str, price: int, db):
    while True:
        user = get_user_work(telegram_id, db)

        if user is None:
            return None

        if datetime.datetime.now().timestamp() >= user.finish:
            db.delete(user)
            db.commit()

            user = get_user(telegram_id, db)

            user.experience += price
            db.commit()
            db.refresh(user)

            print(user.experience, user.status)
            if user.experience >= 1000 and user.experience < 5000:
                user.status = "junior developer"
                db.commit()
                db.refresh(user)
            elif user.experience >= 5000 and user.experience < 10000:
                user.status = "middle developer"
                db.commit()
                db.refresh(user)

            elif user.experience >= 10000:
                user.status = "senior developer"
                db.commit()
                db.refresh(user)
