import sqlalchemy as sa

MetaData = sa.MetaData()


Ticket = sa.Table(
    'ticket', MetaData,
    sa.Column('booking_token', sa.String(length=1000), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date()),
    sa.Column('fly_from', sa.String(length=9)),
    sa.Column('fly_to', sa.String(length=9)),
    sa.UniqueConstraint('date', 'fly_from', 'fly_to', name='unique_ticket_date_fly_from_fly_to')
)