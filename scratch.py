{{ wtf.quick_form(rating_form, button_map={'submit': 'primary'}) }}



# Rating page for each anime
@app.route('/rate', methods=['GET', 'POST'])
@login_required
def rate():
    anime_name = request.args.get('anime_name', None)
    anime = db.session.query(Animes).filter_by(name=anime_name).first()
    user_id = current_user.id

    form = RatingForm(csrf=False)

    if form.validate_on_submit():
        new_rating = form.rating.data
        if new_rating in range(1, 11):
            r = Ratings(anime_name=anime_name, user_rating=new_rating, user_id=user_id)
            db.session.add(r)
            db.session.commit()
            return redirect(url_for('search'))
    return render_template('rate.html', anime=anime, form=form)