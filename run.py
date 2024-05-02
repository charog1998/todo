from init_app import create_app,db


if __name__ == "__main__":
    # fake = Faker('zh_cn')
    # with app.app_context():
    #     # db.create_all()
    #     # py = Category('Python')
    #     # p = Post('Hello Python!', 'Python is pretty cool', py)
    #     # db.session.add(py)
    #     # db.session.add(p)
    #     # db.session.commit()

    #     # 添加模拟信息
    #     # for _ in range(100):
    #     #     user = user = User(
    #     #         username=fake.name(),
    #     #         email=str(random.randint(111111, 999999)) + "@mail.com",
    #     #     )
    #     #     db.session.add(user)
    #     # db.session.commit()

    #     users = User.query.all()
    #     print(users)
    app=create_app()
    # with app.app_context():
    #     db.create_all()
    app.run('0.0.0.0',5000)
