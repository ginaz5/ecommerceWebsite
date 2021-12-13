# E Commerce Website bulid with Django
## Description
The website displays products. Users can add and remove products to/from their cart while also specifying the quantity of each item. They can then enter their address and choose Stripe to handle the payment processing.

## Demo
[Video Demo](https://youtu.be/yPvm-zjzQTs)

## Development Structure
Backend: Python

Framework: Django

Front-end: HTML, CSS, Javascript(Vue.js), Bulma

Database: db.sqlite3

Payment Integration: Stripe


- Use Vue.js and Bulma to create an interactive page and cross-platform support.
- Use Django ORM to communicate with the database
- Integrated Stripe payment for checkout


## UML
![ER_Model](Model.png)


## Fixed Bug List
- Product image display issue. 

Reason: Static file path error, django save upload files to media/uploads/media/uploads

- The total amount of products in the cart was not updated.

Reason: Function totalcost error

- Payment status doesn't update in database when stripe received payment.

Reason: forgot to set payment_status = True when payment is done.

- Cannot delete checkout product in admin, IntegrityError FOREIGN KEY constraint failed

Reason: database design is not consider the situation.


## Reference
[Ecommerce website using Django 3 and Vue.js | Django tutorial series](https://youtube.com/playlist?list=PLpyspNLjzwBmIDrDOaPkLLuy5YDDNW9SA)

[Build an Ecommerce Website with Django](https://www.youtube.com/watch?v=z4USlooVXG0&list=PLLRM7ROnmA9F2vBXypzzplFjcHUaKWWP5)
