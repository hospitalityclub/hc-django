class LegacyRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'hcolddata':
            return 'legacy'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'hcolddata':
            return 'legacy'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'hcolddata':
            return db == 'legacy'
        return None
