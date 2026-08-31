-- ============================================================================
--  Quick menu + honorary doctors — tables generated from the SQLAlchemy models.
--
--  Production has no alembic_version table, so this is DDL only, no stamp.
--  Every statement is IF NOT EXISTS and the whole file is one transaction, so it
--  is safe to run whole and safe to re-run: existing tables are skipped.
--
--  Parents are created before the tables that reference them, so run it top to
--  bottom without reordering.
--
--  NOTE: IF NOT EXISTS skips a table that already exists — it does NOT add
--  missing columns to one. Run the "missing tables" query first (see the message
--  that accompanied this file) to see what is actually absent.
-- ============================================================================

BEGIN;

CREATE TABLE IF NOT EXISTS honorary_doctor (
	id SERIAL NOT NULL, 
	image TEXT, 
	display_order INTEGER NOT NULL, 
	is_active BOOLEAN NOT NULL DEFAULT true, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS ix_honorary_doctor_id ON honorary_doctor (id);

CREATE TABLE IF NOT EXISTS menu_contacts (
	id SERIAL NOT NULL, 
	context VARCHAR(20) NOT NULL, 
	email VARCHAR(200) NOT NULL, 
	is_active BOOLEAN NOT NULL DEFAULT true, 
	PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS ix_menu_contacts_id ON menu_contacts (id);

CREATE TABLE IF NOT EXISTS menu_quick_left_items (
	id SERIAL NOT NULL, 
	url TEXT NOT NULL, 
	display_order INTEGER NOT NULL, 
	is_active BOOLEAN NOT NULL DEFAULT true, 
	PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS ix_menu_quick_left_items_id ON menu_quick_left_items (id);

CREATE TABLE IF NOT EXISTS menu_quick_sections (
	id SERIAL NOT NULL, 
	section_key VARCHAR(50) NOT NULL, 
	display_order INTEGER NOT NULL, 
	is_active BOOLEAN NOT NULL DEFAULT true, 
	PRIMARY KEY (id), 
	UNIQUE (section_key)
);

CREATE INDEX IF NOT EXISTS ix_menu_quick_sections_id ON menu_quick_sections (id);

CREATE TABLE IF NOT EXISTS menu_social_links (
	id SERIAL NOT NULL, 
	platform VARCHAR(50) NOT NULL, 
	url TEXT NOT NULL, 
	context VARCHAR(20) NOT NULL, 
	display_order INTEGER NOT NULL, 
	is_active BOOLEAN NOT NULL DEFAULT true, 
	PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS ix_menu_social_links_id ON menu_social_links (id);

CREATE TABLE IF NOT EXISTS honorary_doctor_tr (
	id SERIAL NOT NULL, 
	doctor_id INTEGER NOT NULL, 
	lang_code VARCHAR(2) NOT NULL, 
	full_name TEXT NOT NULL, 
	description TEXT, 
	created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(doctor_id) REFERENCES honorary_doctor (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_honorary_doctor_tr_doctor_id ON honorary_doctor_tr (doctor_id);
CREATE INDEX IF NOT EXISTS ix_honorary_doctor_tr_id ON honorary_doctor_tr (id);

CREATE TABLE IF NOT EXISTS menu_contact_addresses (
	id SERIAL NOT NULL, 
	contact_id INTEGER NOT NULL, 
	lang_code VARCHAR(5) NOT NULL, 
	address TEXT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(contact_id) REFERENCES menu_contacts (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_menu_contact_addresses_id ON menu_contact_addresses (id);

CREATE TABLE IF NOT EXISTS menu_contact_phones (
	id SERIAL NOT NULL, 
	contact_id INTEGER NOT NULL, 
	phone VARCHAR(50) NOT NULL, 
	display_order INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(contact_id) REFERENCES menu_contacts (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_menu_contact_phones_id ON menu_contact_phones (id);

CREATE TABLE IF NOT EXISTS menu_quick_left_item_translations (
	id SERIAL NOT NULL, 
	item_id INTEGER NOT NULL, 
	lang_code VARCHAR(5) NOT NULL, 
	label VARCHAR(200) NOT NULL, 
	url TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(item_id) REFERENCES menu_quick_left_items (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_menu_quick_left_item_translations_id ON menu_quick_left_item_translations (id);

CREATE TABLE IF NOT EXISTS menu_quick_section_items (
	id SERIAL NOT NULL, 
	section_id INTEGER NOT NULL, 
	url TEXT NOT NULL, 
	display_order INTEGER NOT NULL, 
	is_active BOOLEAN NOT NULL DEFAULT true, 
	PRIMARY KEY (id), 
	FOREIGN KEY(section_id) REFERENCES menu_quick_sections (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_menu_quick_section_items_id ON menu_quick_section_items (id);

CREATE TABLE IF NOT EXISTS menu_quick_section_translations (
	id SERIAL NOT NULL, 
	section_id INTEGER NOT NULL, 
	lang_code VARCHAR(5) NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(section_id) REFERENCES menu_quick_sections (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_menu_quick_section_translations_id ON menu_quick_section_translations (id);

CREATE TABLE IF NOT EXISTS menu_quick_section_item_translations (
	id SERIAL NOT NULL, 
	item_id INTEGER NOT NULL, 
	lang_code VARCHAR(5) NOT NULL, 
	label VARCHAR(200) NOT NULL, 
	url TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(item_id) REFERENCES menu_quick_section_items (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_menu_quick_section_item_translations_id ON menu_quick_section_item_translations (id);

COMMIT;
