from models.models import User as UserModel
from DTO.user import User as UserDTO


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


def change_status(telegram_id: str,status : str, db):
    user = get_user(telegram_id,db)
    user.status = status
    db.commit()
    db.refresh(user)