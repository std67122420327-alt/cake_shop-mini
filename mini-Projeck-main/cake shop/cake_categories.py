categories = [
    'อาหารไทย',
    'อาหารจีน',
    'อาหารญี่ปุ่น',
    'อาหารอีสาน',
    'เครื่องดื่ม',
    'ของหวาน',
    'อาหารทะเล',
    'ฟาสต์ฟู้ด',
    'อาหารเจ',
    'อาหารมังสวิรัติ'
]

from foodapp.models import Category
food_categories = [Category(name=cat) for cat in categories]