# Enable runtime type-checking for the entire deepdoc package
from beartype.claw import beartype_this_package
beartype_this_package()