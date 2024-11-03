from pydantic import BaseModel, EmailStr, Field

class UserData(BaseModel):
    fname: str = Field(min_length=1)
    lname: str = Field(min_length=1)
    email: EmailStr
    
    def to_json(self):
        return {
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
        }
