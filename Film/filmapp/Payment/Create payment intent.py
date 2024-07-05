import stripe
stripe.api_key = "sk_test_51PYJpzRqcphIMLUdEX4uiJIWSk98O67Nmwblktuo5ODxHIlrsOGwPsaYFcnSWzYNeVKAjLAWjpGhZJG9gmL3fbd300Xvot4kHb"
account_id="acct_1PYJpzRqcphIMLUd"


# Tạo một giao dịch mới
# charge = stripe.Charge.create(
#   amount=2000,  # Số tiền tính bằng cents (20.00 USD)
#   currency="usd",  # Đơn vị tiền tệ
#   source="tok_visa",  # Mã token của nguồn thanh toán (thẻ, ví điện tử, v.v.)
#   description="Example charge"
# )

# Lấy mã giao dịch (charge ID)
# charge_id = charge.id
#
# print("Mã giao dịch (charge ID):", charge_id)

# xác nhận giao dịch hoàn chỉnh
# charge.capture()

#lấy thông tin giao dịch
# charge = stripe.Charge.retrieve(
#   #đây là charge_id
#   "ch_3PZ481RqcphIMLUd1jduBwhm",
# )
# print(charge)

#tạo phiên giao dịch nhưng chưa xác nhận còn nhiều field trong đây nữa
# stripe.PaymentIntent.create(
#   amount=1000,
#   currency="usd",
#   payment_method="pm_card_visa",
#   customer="cus_QPfvNpmlt49dYN",
#   description="Account Pay Fee",
#   automatic_payment_methods={"enabled": True},
#   #'Cái này trong profile -> accounts -> id'
#   stripe_account='acct_1PYJpzRqcphIMLUd',
# )
# thấy thông tin thanh toán
# charge = stripe.Charge.retrieve(
#   "ch_3PZ481RqcphIMLUd1jduBwhm",
#   stripe_account=account_id
# )
# print(charge)

#tạo paymen_methods (Chưa hoàn thành)
# stripe.PaymentMethod.create(
#   type="card",
#   card={
#     "number": "4242424242424242",
#     "exp_month": 8,
#     "exp_year": 2026,
#     "cvc": "314",
#   },
# )

