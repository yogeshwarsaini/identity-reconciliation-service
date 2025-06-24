from app.database import db
from app.models import Contact
from sqlalchemy import or_

def process_identity(email=None, phone=None):
    # Step 1: Find existing contacts by email or phone
    matched_contacts = Contact.query.filter(
        or_(
            Contact.email == email,
            Contact.phoneNumber == phone
        )
    ).all()

    if not matched_contacts:
        # Step 2: No existing contact → create primary
        new_contact = Contact(
            email=email,
            phoneNumber=phone,
            linkPrecedence='primary'
        )
        db.session.add(new_contact)
        db.session.commit()

        return {
            "primaryContactId": new_contact.id,
            "emails": [new_contact.email] if new_contact.email else [],
            "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
            "secondaryContactIds": []
        }

    # Step 3: Merge logic – find primary contact among matches
    primary_contact = None
    for contact in matched_contacts:
        if contact.linkPrecedence == 'primary':
            primary_contact = contact
            break

    if not primary_contact:
        # If no primary, pick oldest one as primary
        primary_contact = sorted(matched_contacts, key=lambda c: c.createdAt)[0]
        primary_contact.linkPrecedence = 'primary'
        db.session.commit()

    # Step 4: Create new secondary contact if new data
    already_exists = any(
        c.email == email and c.phoneNumber == phone
        for c in matched_contacts
    )

    if not already_exists:
        new_secondary = Contact(
            email=email,
            phoneNumber=phone,
            linkPrecedence='secondary',
            linkedId=primary_contact.id
        )
        db.session.add(new_secondary)
        db.session.commit()
        matched_contacts.append(new_secondary)

    # Step 5: Build final response
    emails = set()
    phones = set()
    secondary_ids = []

    for contact in matched_contacts:
        if contact.email:
            emails.add(contact.email)
        if contact.phoneNumber:
            phones.add(contact.phoneNumber)
        if contact.linkPrecedence == 'secondary':
            secondary_ids.append(contact.id)

    return {
        "primaryContactId": primary_contact.id,
        "emails": list(emails),
        "phoneNumbers": list(phones),
        "secondaryContactIds": secondary_ids
    }
