from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from app.db.session import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")

TokenDep = Annotated[str, Depends(oauth2_scheme)]
FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
SessionDep = Annotated[Session, Depends(get_session)]
