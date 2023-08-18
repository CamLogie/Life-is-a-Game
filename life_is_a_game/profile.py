from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)

from life_is_a_game.db import get_db, close_db, results_to_dict
from life_is_a_game.points.health_point import HealthPoint
from life_is_a_game.points.life_point import LifePoint
from life_is_a_game.points.money_point import MoneyPoint
from life_is_a_game.points.point_type import PointType
from life_is_a_game.helpers.sql_query_factory import SqlQueryFactory

bp = Blueprint('profile', __name__)

@bp.route('/wallet')
def wallet():
    return render_template('profile/wallet.html')


@bp.route('/point/<additive_operator>/<point_type>/<int:value>', methods=(['POST']))
def add_point(additive_operator, point_type, value):
    """add points to transaction list and update wallet"""

    if additive_operator == 'subtract':
        value = value * -1 
    
    sql_query_factory = SqlQueryFactory()

    user_id = g.user['id']

    match point_type:
        case PointType.HEALTH.value:
            point = HealthPoint(value)
            balance = 'health_points_balance = '
        case PointType.LIFE.value:
            point = LifePoint(value)
            balance = 'life_points_balance = '
        case PointType.MONEY.value:
            point = MoneyPoint(value)
            balance = 'money_points_balance = '

    db = get_db()
    cur = db.cursor()
    

    cur.execute('''
        INSERT INTO transactions (user_id, point_type, val) 
        VALUES %s''', [(user_id, point.point_type, point.val)],
    )
    cur.execute('''
        SELECT SUM(val) FROM transactions 
        WHERE point_type = %s AND user_id = %s''', (point.point_type, user_id,)
    )

    balance = balance + str(cur.fetchone()[0])


    cur.execute(
        sql_query_factory.update_where('wallet', balance, 'user_id = {}'.format(user_id))
    )

    db.commit()
    close_db(db, cur)

    return redirect(url_for('profile.wallet'))

@bp.route('/add_health_point/<int:value>')
def add_health_point(value):
    """add health point to user wallet and redirect to wallet"""
    db = get_db()
    cur = db.cursor()
    user_id = g.user['id']

    hp = HealthPoint(value, PointType.HEALTH.value)
    cur.execute('''
        INSERT INTO transactions (user_id, point_type, val) 
        VALUES %s''', [(user_id, hp.point_type, hp.val)],
    )
    cur.execute('''
        SELECT SUM(val) FROM transactions 
        WHERE point_type = %s AND user_id = %s''', (hp.point_type, user_id,)
    )
    hp_sum = cur.fetchone()[0]
    cur.execute('''
        UPDATE wallet
        SET health_points_balance = %s 
        WHERE user_id = %s''', ((hp_sum, user_id,))
    )

    db.commit()
    close_db(db, cur)

    return redirect(url_for('profile.wallet'))

@bp.route('/add_life_point/<int:value>')
def add_life_point(value):
    """add life point to user wallet and redirect to wallet"""
    db = get_db()
    cur = db.cursor()
    user_id = g.user['id']

    lp = LifePoint(value, PointType.LIFE.value)
    cur.execute('''
        INSERT INTO transactions (user_id, point_type, val) 
        VALUES %s''', [(user_id, lp.point_type, lp.val)],
    )
    cur.execute('''
        SELECT SUM(val) FROM transactions 
        WHERE point_type = %s AND user_id = %s''', (lp.point_type, user_id,)
    )
    lp_sum = cur.fetchone()[0]
    cur.execute('''
        UPDATE wallet
        SET life_points_balance = %s 
        WHERE user_id = %s''', ((lp_sum, user_id,))
    )

    db.commit()
    close_db(db, cur)

    return redirect(url_for('profile.wallet'))

@bp.route('/add_money_point/<int:value>')
def add_money_point(value):
    """add life point to user wallet and redirect to wallet"""
    db = get_db()
    cur = db.cursor()
    user_id = g.user['id']

    mp = MoneyPoint(value, PointType.MONEY.value)
    cur.execute('''
        INSERT INTO transactions (user_id, point_type, val) 
        VALUES %s''', [(user_id, mp.point_type, mp.val)],
    )
    cur.execute('''
        SELECT SUM(val) FROM transactions 
        WHERE point_type = %s AND user_id = %s''', (mp.point_type, user_id,)
    )
    mp_sum = cur.fetchone()[0]
    cur.execute('''
        UPDATE wallet
        SET money_points_balance = %s 
        WHERE user_id = %s''', ((mp_sum, user_id,))
    )

    db.commit()
    close_db(db, cur)

    return redirect(url_for('profile.wallet'))

def load_user_wallet(cur, user_id):
    cur.execute('''SELECT * FROM wallet WHERE user_id = %s''', (user_id,))
    wallet_data = results_to_dict(cur)

    return wallet_data
