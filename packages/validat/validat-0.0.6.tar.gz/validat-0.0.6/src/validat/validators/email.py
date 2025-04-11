from validat.exceptions.base import EmailValidationError, ErrorRaiser


def validate_email(
    email: str,
    raise_exception: bool = False,
    username: str = None,
    domain_name: str = None,
    tld: str = None,
) -> bool:
    """Validate email adress.

    Args:
        **email** (str): Email address \n
        **raise_exception** (bool, optional): Raise exception if validation fails. Defaults to False. \n
        **username** (str, optional): Username to validate. Defaults to None. \n
        **domain_name** (str, optional): Domain name to validate. Defaults to None. \n
        **tld** (str, optional): TLD(Top-Level-Domain) to validate. Defaults to None. \n

    Returns:
        **bool**: True if email is valid. False if not.
    """
    error = ErrorRaiser(
        raise_exception=raise_exception, exception_type=EmailValidationError
    )

    if not email:
        return error("Email address cannot be empty")

    forbidden = set("!#$%^&*()")
    at_sign_count = email.count("@")

    if at_sign_count != 1:
        return error("Email address must have exactly one @ sign")

    if len(email) > 254:
        return error("Email address cannot have more than 254 characters")

    if forbidden.intersection(set(email)):
        return error("Email address contains unreadable characters.")

    if ".." in email:
        return error("Email address cannot contain two dots together")

    if " " in email:
        return error("Email adress cannot contain spaces")

    at_index = email.find("@")
    splitted_username = email[:at_index]
    splitted_domain = email[at_index + 1 :]

    if not splitted_username:
        return error("Email address must contain a username")

    if "." == splitted_username[0]:
        return error("Email address cannot begin with a dot")

    if "." == splitted_username[-1]:
        return error("Username cannot end with a dot")

    if not splitted_domain:
        return error("Email address must contain a domain")

    if "." not in splitted_domain:
        return error("Domain must have at least one dot")

    if "." == splitted_domain[0]:
        return error("Domain cannot begin with a dot")

    if "." == splitted_domain[-1]:
        return error("Email address cannot end with a dot")

    splitted_tld = splitted_domain[splitted_domain.find(".") + 1 :]
    splitted_domain_name = splitted_domain[: splitted_domain.find(".")]

    if len(splitted_tld) < 2:
        return error("TLD must be no shorter than 2 characters")

    if username is not None and splitted_username != username:
        return error("Email address has different username")

    if domain_name is not None and splitted_domain_name != domain_name:
        return error("Email address has different domain name")

    if tld is not None and splitted_tld != tld:
        return error("Email address has different top level domain")

    return True
