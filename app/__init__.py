from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    with app.app_context():
        from .routes import (
            main_routes, feedback_routes, task_info_routes, status_routes,
            bag_routes, skill_routes, accept_routes, time_routes, others_routes
        )
        app.register_blueprint(main_routes.bp)
        app.register_blueprint(feedback_routes.bp)
        app.register_blueprint(task_info_routes.bp)
        app.register_blueprint(status_routes.bp)
        app.register_blueprint(bag_routes.bp)
        app.register_blueprint(skill_routes.bp)
        app.register_blueprint(accept_routes.bp)
        app.register_blueprint(time_routes.bp)
        app.register_blueprint(others_routes.bp)
        return app
