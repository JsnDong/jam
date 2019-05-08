DEPT_CHOICES = (
	(None, 'SELECT'),
	('brass', 'BRASS'),
	('strings', 'STRINGS'),
	('woodwind', 'WOODWIND'),
	('percussion', 'PERCUSSION'),
	('keyboard', 'KEYBOARD'),
	('other', 'OTHER'),
)

SHIPPING_CHOICES = (
	(None, 'SELECT'),
	('standard', 'STANDARD'),
	('twoday', 'TWO-DAY'),
	('oneday', 'ONE-DAY'),
)

DELIVERY_STATUS_CHOICES = (
	(None, 'SELECT'),
	('processing', 'PROCESSING'),
	('shippped', 'SHIPPED'),
	('delivered', 'DELIVERED')
)
