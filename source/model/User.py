from dataclasses import dataclass, field
from enums.LanguageEnum import LanguageEnum
from enums.UserTierEnum import UserTierEnum
from model.Profile import Profile
from datetime import datetime

# A User entity.
@dataclass
class User:
    Id: str
    Username: str
    FirstName: str = ""
    LastName: str = ""
    EmailEnabled: bool = True
    SmsEnabled: bool = True
    TargetedAdvertEnabled: bool = True
    LanguagePreference: LanguageEnum = LanguageEnum.English
    Friends: dict[str, bool] = field(default_factory=dict)
    University: str = ""
    Major: str = ""
    Profile: Profile = None
    TierEnum: UserTierEnum = UserTierEnum.Standard
    _LastLoginTimestamp: datetime = field(default_factory=datetime.now)
    _SignUpTimestamp: datetime = field(default_factory=datetime.now)

    # Hydrates a User entity using a pyrebase response value and returns it.
    def HydrateUser(user):
        return User(
                Id = UserHydrator.HydrateProp(user, "Id"),
                Username = UserHydrator.HydrateProp(user, "Username"),
                FirstName = UserHydrator.HydrateProp(user, "FirstName"),
                LastName = UserHydrator.HydrateProp(user, "LastName"),
                EmailEnabled = UserHydrator.HydrateProp(user, "EmailEnabled"),
                SmsEnabled = UserHydrator.HydrateProp(user, "SmsEnabled"),
                TargetedAdvertEnabled = UserHydrator.HydrateProp(user, "TargetedAdvertEnabled"),
                LanguagePreference = UserHydrator.HydrateProp(user, "LanguagePreference"),
                Friends = UserHydrator.HydrateProp(user, "Friends"),
                University = UserHydrator.HydrateProp(user, "University"),
                Major = UserHydrator.HydrateProp(user, "Major"),
                Profile = UserHydrator.HydrateProp(user, "Profile"),
                TierEnum = UserHydrator.HydrateProp(user, "TierEnum"),
                _LastLoginTimestamp = UserHydrator.HydrateProp(user, "_LastLoginTimestamp"),
                _SignUpTimestamp = UserHydrator.HydrateProp(user, "_SignUpTimestamp")
            )

class UserHydrator:
    
    # A dictionary to maintain the User entity's property name (key) and its type (value).
    _userAttributes: dict[str, str] = {
        "Id": "str",
        "Username": "str",
        "FirstName": "str",
        "LastName": "str",
        "EmailEnabled": "bool",
        "SmsEnabled": "bool",
        "TargetedAdvertEnabled": "bool",
        "LanguagePreference": "LanguageEnum",
        "Friends": "dict[str, bool]",
        "University": "str",
        "Major": "str",
        "Profile": "Profile",
        "TierEnum": "UserTierEnum",
        "_LastLoginTimestamp": "datetime",
        "_SignUpTimestamp": "datetime"
    }
    
    # Hydrates an individual property for the User entity.
    def HydrateProp(user, prop: str):
        if prop not in UserHydrator._userAttributes.keys():
            raise Exception(f"Property {prop} not defined for entity: User")
        
        propType: str = UserHydrator._userAttributes.get(prop)
        value = None
        
        try:
            pyreValue = user.val()[prop]
            value = UserHydrator.Cast(pyreValue, propType)
        except:
            value = UserHydrator.GetDefaultValue(prop)
        
        if value == None: raise Exception(f"Could not hydrate prop: {prop} for User")
        
        return value
    
    # Handles conversion to a certain type.
    def Cast(pyreValue, propType):
        if propType == "Profile":
            profile: Profile = Profile.HydrateProfile(pyreValue)
            return profile
        
        if propType == "UserTierEnum":
            enumName: str = str(pyreValue).lstrip("UserTierEnum.")
            tierEnum: UserTierEnum = UserTierEnum[enumName]
            return tierEnum
        
        if propType == "datetime":
            datetimeValue: datetime = datetime.fromisoformat(pyreValue)
            return datetimeValue
        
        return pyreValue
        
    # Gets the default value for a property on the User entity based on its type.
    def GetDefaultValue(prop: str):
        propType: str = UserHydrator._userAttributes.get(prop)

        if propType == "str": return ""
        elif propType == "bool": return True
        elif propType == "LanguageEnum": return LanguageEnum.English
        elif propType == "dict[str, bool]": return {}
        elif propType == "Profile": return Profile()
        elif propType == "UserTierEnum": return UserTierEnum.Standard
        elif propType == "datetime": return datetime.min
        else: return None