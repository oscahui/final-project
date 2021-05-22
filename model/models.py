def create_bitcoin_data_classes(db):
    class BITCOIN_DATA(db.Model):
        __tablename__ = 'bitcoin_data'

        date = db.Column(db.DateTime, primary_key=True)
        close = db.Column(db.Float)
        real = db.Column(db.Boolean)
        ma_5 = db.Column(db.Float)
        ma_10 = db.Column(db.Float)
        ma_20 = db.Column(db.Float)
        ma_30 = db.Column(db.Float)
        ma_60 = db.Column(db.Float)
        ma_90 = db.Column(db.Float)
        ma_180 = db.Column(db.Float)
        ma_240 = db.Column(db.Float)
        ma_360 = db.Column(db.Float)         

        def __repr__(self):
            return f'<bitcoin_data {self.id}>'
    
    return BITCOIN_DATA

def create_mix_data_classes(db):
    class MIX_DATA(db.Model):
        __tablename__ = 'mix_data'

        date = db.Column(db.DateTime, primary_key=True)
        close = db.Column(db.Float)
        real = db.Column(db.Boolean)
        gold = db.Column(db.Float)
        comp = db.Column(db.Float)
        spx = db.Column(db.Float)
        indu = db.Column(db.Float)
        oil = db.Column(db.Float)
        btc_diff = db.Column(db.Float)
        gold_diff = db.Column(db.Float)
        comp_diff = db.Column(db.Float)
        spx_diff = db.Column(db.Float)
        indu_diff = db.Column(db.Float)
        oil_diff = db.Column(db.Float)
        btc_diffpct = db.Column(db.Float)
        gold_diffpct = db.Column(db.Float)
        comp_diffpct = db.Column(db.Float)
        spx_diffpct = db.Column(db.Float)
        indu_diffpct = db.Column(db.Float)
        oil_diffpct = db.Column(db.Float)       

        def __repr__(self):
            return f'<mix_data {self.id}>'
    
    return MIX_DATA



 
