from flask import render_template, request, flash, redirect
# flash permet d'afficher des messages d'erreur ou de succès.
# redirect permet de rediriger vers une page spécifiée.

from sqlalchemy import or_
# Import de "or_" pour utiliser l'opérateur boléen "or" pour les requêtes dans le BDD lors de la recherche simple.
from ..app import app, login, db
# Import des variables "app", "login", "db" pour instancier notre application.
from ..modeles.donnees import Brique, Plan, Theme, Authorship
# Import des classes "Brique", "Plan", "Theme", "Authorship", du fichier "donnees.py".
from ..modeles.utilisateurs import User
# Import de la classe "User" du fichier "utilisateurs.py".
from ..constantes import LIEUX_PAR_PAGE
# Récupération de la constante du fichier "constantes.py".

from flask_login import login_user, current_user, logout_user, login_required
# Pour gérer les connexions et les déconnexions des utilisateurs.

# On calcule le nombre total de briques dans la base de données. Cela permettra de gérer les fonctionnalités "page précédente" et "page suivante" dans les notices des briques, des plans, des thèmes.
brique = Brique.query.order_by(Brique.brique_id).all()
nbr_b = brique[-1].brique_id
# On calcule le nombre total de plans dans la base de données.
plan = Plan.query.order_by(Plan.plan_id).all()
nbr_p = plan[-1].plan_id
# On calcule le nombre total de thèmes dans la base de données.
theme = Theme.query.order_by(Theme.theme_id).all()
nbr_t = theme[-1].theme_id

@app.route("/")
def accueil():
    """ Route permettant l'affichage de la page d'accueil
    :return: le template de la page d'accueil (accueil.html)
    """
    return render_template("pages/accueil.html")
    # La fonction render_template a premier argument qui est le chemin du template

@app.route("/brique/<int:brique_id>")
def brique(brique_id):
    """ Route permettant l'affichage d'une notice d'une brique
    :param brique_id: l'identifiant de la brique
    :type brique_id:int
    :return: le template de la notice d'une brique (brique.html)
    """
    unique_brique = Brique.query.get(brique_id)
    return render_template("pages/brique.html", brique=unique_brique, nbr_b=nbr_b)

@app.route("/plan/<int:plan_id>")
def plan(plan_id):
    """ Route permettant l'affichage d'une notice d'un plan de construction
    :param plan_id: l'identifiant du plan
    :type plan_id:int
    :return: le template de la notice d'un plan (plan.html)
    """
    unique_plan = Plan.query.get(plan_id)
    return render_template("pages/plan.html", plan=unique_plan, nbr_p=nbr_p)

@app.route("/theme/<int:theme_id>")
def theme(theme_id):
    """ Route permettant l'affichage d'une notice d'un thème
    :param theme_id: l'identifiant du thème
    :type theme_id:int
    :return: le template de la notice d'un thème (theme.html)
    """
    unique_theme = Theme.query.get(theme_id)
    return render_template("pages/theme.html", theme=unique_theme, nbr_t=nbr_t)

@app.route("/Les_index/index_plans")
def index_plans():
    """ Route permettant l'affichage de la page de l'index des plans'.
    :return: le template de l'index des plans' (index_plans.html)
    """
    # On préfèrera l'utilisation de .get() ici
    #   qui nous permet d'éviter un if long (if "clef" in dictionnaire and dictonnaire["clef"])
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Plan.query.paginate(page=page, per_page=LIEUX_PAR_PAGE)

    return render_template(
        "pages/index_plans.html",
        resultats=resultats
    )

@app.route("/Les_index/index_briques")
def index_briques():
    """ Route permettant l'affichage de la page de l'index des briques'.
    :return: le template de l'index des briques' (index_briques.html)
    """

    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Brique.query.paginate(page=page, per_page=LIEUX_PAR_PAGE)

    return render_template(
        "pages/index_briques.html",
        resultats=resultats
    )

@app.route("/Les_index/index_themes")
def index_themes():
    """ Route permettant l'affichage de la page de l'index des thèmes'.
    :return: le template de l'index des thèmes' (index_themes.html)
    """

    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = Theme.query.paginate(page=page, per_page=LIEUX_PAR_PAGE)

    return render_template(
        "pages/index_themes.html",
        resultats=resultats
    )

@app.route("/recherche")
def recherche():
    """ Route permettant d'afficher une page de recherche simple grâce à une requête dans la table "Plan".
    :return: le template de la page des résultats de la recherche simple (recherche.html)
    """

    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # On crée une liste vide de résultat (qui restera vide par défaut
    #   si on n'a pas de mot clé)
    resultats = []
    # On fait de même pour le titre de la page
    titre = "Recherche"
    if motclef:
        resultats = Plan.query.filter(
           or_(
            Plan.plan_ensemble.like("%{}%".format(motclef)),
            Plan.plan_date_sortie.like("%{}%".format(motclef)),
            Plan.briques.any((Brique.brique_element).like("%{}%".format(motclef))),
            Plan.theme.has((Theme.theme_nom).like("%{}%".format(motclef))),
            )
        ).paginate(page=page, per_page=LIEUX_PAR_PAGE)

        titre = "Résultat pour la recherche `" + motclef + "`"
    return render_template("pages/recherche.html", resultats=resultats, titre=titre, keyword=motclef)

@app.route('/recherche_plans', methods=["POST", "GET"])
def recherche_plans():
    """ Route permettant d'afficher une page de recherche avancee pour les plans grâce à une requête dans la table "Plan".
    :return: le template de la page du formulaire pour la recherche avancee des plans (recherche_plans.html) et le template de la page des résultats pour la recherche avancee des plans (resultats_plans.html)
    """
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if request.method == "POST":

        titre = "Recherche"

        keyword="test"
        question=Plan.query

        plan_ensemble = request.form.get("plan_ensemble", None)
        plan_date_sortie=request.form.get("plan_date_sortie",None)
        plan_theme=request.form.get("plan_theme", None)
        brique = request.form.get("brique", None)

        if plan_ensemble:
            question=question.filter(Plan.plan_ensemble.like("%{}%".format(plan_ensemble)))
        if plan_date_sortie:
            question=question.filter(Plan.plan_date_sortie.like("%{}%".format(plan_date_sortie)))
        if plan_theme:
            question=question.filter(Plan.theme.has(Theme.theme_nom.like("%{}%".format(plan_theme))))
        if brique:
            question=question.filter(Plan.briques.any(Brique.brique_element.like("%{}%".format(brique))))
        question=question.paginate(page=page)

        return render_template(
            "pages/resultats_plans.html",
            resultats=question,
            titre=titre,
            keyword=keyword
        )


    return render_template("pages/recherche_plans.html")

@app.route('/recherche_briques', methods=["POST", "GET"])
def recherche_briques():
    """ Route permettant d'afficher une page de recherche avancee pour les briques grâce à une requête dans la table "Brique".
    :return: le template de la page du formulaire pour la recherche avancee des briques (recherche_briques.html) et le template de la page des résultats pour la recherche avancee des briques (resultats_briques.html)
    """
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if request.method == "POST":

        titre = "Recherche"

        keyword="test"
        question=Brique.query

        brique_element = request.form.get("brique_element", None)
        plan=request.form.get("plan", None)

        if brique_element:
            question=question.filter(Brique.brique_element.like("%{}%".format(brique_element)))
        if plan:
            question=question.filter(Brique.plans.any(Plan.plan_ensemble.like("%{}%".format(plan))))
        question=question.paginate(page=page)

        return render_template(
            "pages/resultats_briques.html",
            resultats=question,
            titre=titre,
            keyword=keyword
        )


    return render_template("pages/recherche_briques.html")

@app.route("/glossaire")
def glossaire():
    """ Route permettant d'afficher la page du glossaire.
    :return: le template de la page du glossaire (glossaire.html)
    """
    return render_template("pages/glossaire.html")

@app.route("/a_propos")
def a_propos():
    """ Route permettant d'afficher la page "A propos".
    :return: le template de la page "A propos" (a_propos.html)
    """
    return render_template("pages/a_propos.html")

@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    :return: le template du formulaire d'inscription ou redirect : redirection vers la page d'accueil
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    :return: le template du formulaire de connexion ou redirect : redirection vers la page d'accueil
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")
login.login_view = 'connexion'

@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """ Route gérant les deconnexions
    :return: redirect : redirection vers la page d'accueil
    """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")

@app.route("/supprimer_brique/<int:brique_id>", methods=["POST", "GET"])
@login_required
def supprimer_brique(brique_id):
    """
    Route permettant la suppression d'une brique et de ses données dans la BDD
    :param brique_id: l'identifiant de la brique dans la BDD
    :type brique_id: int
    :return: le template du formulaire de suppression d'une brique (supprimer_brique.html) ou redirect : redirection vers la page d'accueil
    """
    suppr_brique = Brique.query.get(brique_id)

    if request.method == "POST":
        # on fait appel à la méthode statique ".supprimer_brique" du fichier "donnees.py"
        statut = Brique.supprimer_brique(
            brique_id=brique_id
        )

        if statut is True:
            flash("Suppression réussie", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué. Réessayez !", "error")
            return redirect("/")
    else:
        return render_template("pages/supprimer_brique.html", suppr_brique=suppr_brique)

@app.route("/supprimer_plan/<int:plan_id>", methods=["POST", "GET"])
@login_required
def supprimer_plan(plan_id):
    """Route permettant la suppression d'un plan et de ses données dans la BDD
    :param plan_id: l'identifiant du plan dans le BDD
    :type plan_id: int
    :return: le template du formulaire de suppression d'un plan (supprimer_plan.html) ou redirect : redirection vers la page d'accueil
    """

    suppr_plan = Plan.query.get(plan_id)

    if request.method == "POST":
        # on fait appel à la méthode statique ".supprimer_plan" du fichier "donnees.py"
        statut = Plan.supprimer_plan(
            plan_id=plan_id
        )

        if statut is True:
            flash("Suppression réussie", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué. Réessayez !", "error")
            return redirect("/")
    else:
        return render_template("pages/supprimer_plan.html", suppr_plan=suppr_plan)

@app.route("/supprimer_theme/<int:theme_id>", methods=["POST", "GET"])
@login_required
def supprimer_theme(theme_id):
    """ Route permettant la suppression d'un thème et de ses données dans la BDD
    :param theme_id: l'identifiant de la thème
    :type theme_id: int
    :return: le template du formulaire de suppression d'un thème (supprimer_theme.html) ou redirect : redirection vers la page d'accueil
    """

    suppr_theme = Theme.query.get(theme_id)

    if request.method == "POST":
        # on fait appel à la méthode statique ".supprimer_theme" du fichier "donnees.py"
        statut = Theme.supprimer_theme(
            theme_id=theme_id
        )

        if statut is True:
            flash("Suppression réussie", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué. Réessayez !", "error")
            return redirect("/")
    else:
        return render_template("pages/supprimer_theme.html", suppr_theme=suppr_theme)

@app.route("/plan/<int:plan_id>/update", methods=["GET", "POST"])
@login_required
def maj_plan(plan_id):
    """Route permettant la mise à jour des données d'un plan et l'enregistrement des informations de la modification effectuée dans la table "Authorship"
    :param plan_id: l'identifiant du plan dans le BDD
    :type plan_id: int
    :return: le template du formulaire de mise à jour des données d'un plan (maj_plan.html)
    """
    mon_plan = Plan.query.get_or_404(plan_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        # J"ai un formulaire
        if not request.form.get("plan_ensemble", "").strip():
            erreurs.append("Veuillez renseigner le numéro d'ensemble du plan.")
        if not request.form.get("plan_titre", "").strip():
            erreurs.append("Veuillez renseigner le titre en français du plan.")
        if not request.form.get("plan_date_sortie", "").strip():
            erreurs.append("Veuillez renseigner l'année de la date de sortie du plan.")
        if not request.form.get("plan_theme", "").strip():
            erreurs.append("Veuillez renseigner le thème du plan.")
        if not request.form.get("plan_source", "").strip():
            erreurs.append("Veuillez renseigner le lien vers le site Lego.")

        if not erreurs:
            print("Faire ma modifications")
            mon_plan.plan_ensemble = request.form["plan_ensemble"]
            mon_plan.plan_titre = request.form["plan_titre"]
            mon_plan.plan_date_sortie = request.form["plan_date_sortie"]
            mon_plan.plan_theme = request.form["plan_theme"]
            mon_plan.plan_source = request.form["plan_source"]

            db.session.add(mon_plan)
            db.session.add(Authorship(p=mon_plan, u=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/maj_plan.html",
        p=mon_plan,
        erreurs=erreurs,
        updated=updated
    )


@app.route("/brique/<int:brique_id>/update", methods=["GET", "POST"])
@login_required
def maj_brique(brique_id):
    """Route permettant la mise à jour des données d'une brique et l'enregistrement des informations de la modification effectuée dans la table "Authorship"
    :param brique_id: l'identifiant de la brique dans le BDD
    :type brique_id: int
    :return: le template du formulaire de mise à jour des données d'une brique (maj_brique.html)
    """
    ma_brique = Brique.query.get_or_404(brique_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        # J"ai un formulaire
        if not request.form.get("brique_element", "").strip():
            erreurs.append("Veuillez renseigner le numéro d'élément de la brique.")
        if not request.form.get("brique_nom", "").strip():
            erreurs.append("Veuillez renseigner le nom officiel de la brique.")

        if not erreurs:
            print("Faire ma modifications")
            ma_brique.brique_element = request.form["brique_element"]
            ma_brique.brique_nom = request.form["brique_nom"]

            db.session.add(ma_brique)
            db.session.add(Authorship(b=ma_brique, u=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/maj_brique.html",
        b=ma_brique,
        erreurs=erreurs,
        updated=updated
    )


@app.route("/theme/<int:theme_id>/update", methods=["GET", "POST"])
@login_required
def maj_theme(theme_id):
    """Route permettant la mise à jour des données d'un thème et l'enregistrement des informations de la modification effectuée dans la table "Authorship"
    :param theme_id: l'identifiant d'un thème dans le BDD
    :type theme_id: int
    :return: le template du formulaire de mise à jour des données d'un theme (maj_theme.html)
    """
    mon_theme = Theme.query.get_or_404(theme_id)

    erreurs = []
    updated = False

    if request.method == "POST":
        # J"ai un formulaire
        if not request.form.get("theme_nom", "").strip():
            erreurs.append("Veuillez renseigner le nom du thème.")

        if not erreurs:
            print("Faire ma modifications")
            mon_theme.theme_nom = request.form["theme_nom"]

            db.session.add(mon_theme)
            db.session.add(Authorship(t=mon_theme, u=current_user))
            db.session.commit()
            updated = True

    return render_template(
        "pages/maj_theme.html",
        t=mon_theme,
        erreurs=erreurs,
        updated=updated
    )

@app.route("/formulaire/formulaire_theme", methods=["GET", "POST"])
@login_required
def formulaire_theme():
    """Route menant au formulaire d'ajout d'un thème dans la BDD
    :return: le template du formulaire d'ajout d'un thème (formulaire_theme.html) ou redirect : redirection vers la page d'accueil
    """

    # Ajout d'un theme
    if request.method == "POST":
        # on fait appel à la méthode statique ".ajout_theme" du fichier "donnees.py"
        statut, informations = Theme.ajout_theme(
        ajout_theme_id = request.form.get("ajout_theme_id", None),
        ajout_theme_nom = request.form.get("ajout_theme_nom", None)
        )

        if statut is True:
            flash("Ajout d'un nouveau theme", "success")
            return redirect("/")
        else:
            flash("L'ajout a échoué pour les raisons suivantes : " + ", ".join(informations), "danger")
            return render_template("pages/formulaire_theme.html")
    else:
        return render_template("pages/formulaire_theme.html")

@app.route("/formulaire/formulaire_brique", methods=["GET", "POST"])
@login_required
def formulaire_brique():
    """Route menant au formulaire d'ajout d'une brique dans la BDD
    :return: le template du formulaire d'ajout d'une brique (formulaire_brique.html) ou redirect : redirection vers la page d'accueil
    """
    # Ajout d'une brique
    if request.method == "POST":
        # on fait appel à la méthode statique ".ajout_brique" du fichier "donnees.py"
        statut, informations = Brique.ajout_brique(
        ajout_brique_id=request.form.get("ajout_brique_id", None),
        ajout_brique_element=request.form.get("ajout_brique_element", None),
        ajout_brique_nom = request.form.get("ajout_brique_nom", None)
        )

        if statut is True:
            flash("Ajout d'une nouvelle brique", "success")
            return redirect("/")
        else:
            flash("L'ajout a échoué pour les raisons suivantes : " + ", ".join(informations), "danger")
            return render_template("pages/formulaire_brique.html")
    else:
        return render_template("pages/formulaire_brique.html")


@app.route("/formulaire/formulaire_plan", methods=["GET", "POST"])
@login_required
def formulaire_plan():
    """Route menant au formulaire d'ajout d'un plan dans la BDD
    :return: le template du formulaire d'ajout d'un plan (formulaire_plan.html) ou redirect : redirection vers la page d'accueil
    """

    # Ajout d'un plan
    if request.method == "POST":
        # on fait appel à la méthode statique ".ajout_plan" du fichier "donnees.py"
        statut, informations = Plan.ajout_plan(
        ajout_plan_id = request.form.get("ajout_plan_id", None),
        ajout_plan_ensemble = request.form.get("ajout_plan_ensemble", None),
        ajout_plan_titre = request.form.get("ajout_plan_titre", None),
        ajout_plan_theme=request.form.get("ajout_plan_theme", None),
        ajout_plan_date_sortie = request.form.get("ajout_plan_date_sortie", None),
        ajout_plan_source= request.form.get("ajout_plan_source", None)
        )

        if statut is True:
            flash("Ajout d'un nouveau plan", "success")
            return redirect("/")
        else:
            flash("L'ajout a échoué pour les raisons suivantes : " + ", ".join(informations), "danger")
            return render_template("pages/formulaire_plan.html")
    else:
        return render_template("pages/formulaire_plan.html")

@app.route("/formulaire/formulaire_association", methods=["GET", "POST"])
@login_required
def formulaire_association():
    """Route menant au formulaire d'ajout d'une association d'une brique et d'un plan
    :return: le template du formulaire d'ajout d'une association d'une brique et d'un plan (formulaire_association.html) ou redirect : redirection vers la page d'accueil
    """
    # Ajout d'un plan
    if request.method == "POST":
        # on fait appel à la méthode statique ".association_plan_brique" du fichier "donnees.py"
        statut, informations = Plan.association_plan_brique(
        plan_id = request.form.get("plan_id", None),
        brique_id = request.form.get("brique_id", None)
        )

        if statut is True:
            flash("Ajout d'une nouvelle association", "success")
            return redirect("/")
        else:
            flash("L'ajout a échoué. " + " ".join(informations), "danger")
            return render_template("pages/formulaire_association.html")
    else:
        return render_template("pages/formulaire_association.html")
