# datetime permet d'afficher l'historique des modifications
import datetime
# On importe la base de données SQLite qu'on stocke dans une variable appelée "db".
from .. app import db

# On a besoin d'un ORM(Object-Relational-Mapping) pour interroger la base de données.

# Table contenant les informations sur les modifications réalisées par les utilisateurs.
class Authorship(db.Model):
    authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    authorship_brique_id = db.Column(db.Integer, db.ForeignKey('brique.brique_id'))
    authorship_plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'))
    authorship_theme_id = db.Column(db.Integer, db.ForeignKey('theme.theme_id'))
    authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    u = db.relationship("User", back_populates="authorships")
    b = db.relationship("Brique", back_populates="authorships")
    p = db.relationship("Plan", back_populates="authorships")
    t = db.relationship("Theme", back_populates="authorships")

# "Contenir" est une table d'association. Cette table permet d'établir une relation de type many-to-many entre les tables "Brique" et "Plan".
Contenir = db.Table("Contenir",
    db.Column("contenir_brique_id", db.Integer, db.ForeignKey("brique.brique_id"), primary_key=True),
    db.Column("contenir_plan_id", db.Integer, db.ForeignKey("plan.plan_id"), primary_key=True))

# Table contenant les informations des briques des plans : numéro d'élément; nom officiel.
class Brique(db.Model):
    brique_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    brique_element = db.Column(db.Integer)
    brique_nom = db.Column(db.Text)
    #Pour créer les relations d'associations, on a ajouté "secondary" et "Contenir" (nom de la table d'association),
    plans = db.relationship('Plan', secondary=Contenir, back_populates='briques')
    # Pour créer les relations construites à partir de clefs étrangères, on a utilisé "back_populates" et le nom de la table associée. L'initiale du nom de la table est en majuscule.
    authorships = db.relationship("Authorship", back_populates="b")


    # On utilise une méthode statique afin de pouvoir appeler la fonction "ajout_brique" dans notre fichier generic.py.
    @staticmethod
    def ajout_brique(ajout_brique_id, ajout_brique_element, ajout_brique_nom):
        """Fonction qui permet d'ajouter une nouvelle brique dans la BDD
        :param ajout_brique_id: l'identifiant d'une nouvelle brique
        :type ajout_brique_id: int, text
        :param ajout_brique_element: le numéro d'élément d'une nouvelle brique
        :type ajout_brique_element: int, text
        :param ajout_brique_nom: le nom d'une nouvelle brique
        :type ajout_brique_nom: text
        """
        erreurs = []
        if not ajout_brique_id:
            erreurs.append("Veuillez renseigner l'identifiant de la brique.")
        if not ajout_brique_element:
            erreurs.append("Veuillez renseigner le numéro d'élément de la brique.")
        if not ajout_brique_nom:
            erreurs.append(
                "Veuillez renseigner le nom de la brique.")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Brique (champs correspondant aux paramètres du modèle)
        nouvelle_brique = Brique(brique_id=ajout_brique_id,
                                 brique_element=ajout_brique_element,
                              brique_nom=ajout_brique_nom)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(nouvelle_brique)
            db.session.commit()
            return True, nouvelle_brique

        except Exception as erreur:
            return False, [str(erreur)]

    # On utilise une méthode statique afin de pouvoir appeler la fonction "supprimer_brique" dans notre fichier generic.py.
    @staticmethod
    def supprimer_brique(brique_id):
        """Fonction qui permet de supprimer une brique dans la BDD
        :param brique_id: l'identifiant d'une brique
        :type brique_id: int
        :return: True or False et un message d'erreur
        :rtype: booleans, text
        """

        suppr_brique = Brique.query.get(brique_id)

        try:
            db.session.delete(suppr_brique)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

# Table contenant les informations pour les plans de construction : numéro d'ensemble ; titre(en français) ; la date de sortie ; thème ; lien vers le site LEGO.
class Plan(db.Model):
    plan_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    plan_ensemble = db.Column(db.Integer)
    plan_titre = db.Column(db.Text)
    plan_date_sortie = db.Column(db.Integer, nullable=False)
    plan_theme = db.Column(db.Integer, db.ForeignKey('theme.theme_id'))
    plan_source = db.Column(db.Text, nullable=False)
    theme = db.relationship("Theme", back_populates="plan")
    briques = db.relationship('Brique', secondary=Contenir, back_populates='plans')
    authorships = db.relationship("Authorship", back_populates="p")

    # On utilise une méthode statique afin de pouvoir appeler la fonction "ajout_plan" dans notre fichier generic.py.
    @staticmethod
    def ajout_plan(ajout_plan_id, ajout_plan_ensemble, ajout_plan_titre, ajout_plan_date_sortie, ajout_plan_theme, ajout_plan_source):
        """Fonction qui permet d'ajouter un nouveau plan dans la BDD
        :param ajout_plan_id: l'identifiant d'un nouveau plan
        :type ajout_plan_id: int, text
        :param ajout_plan_ensemble: le numéro d'ensemble d'un nouveau plan
        :type ajout_plan_ensemble: int, text
        :param ajout_plan_titre: le titre d'un nouveau plan
        :type ajout_plan_titre: text
        :param ajout_plan_date_sortie: la date de sortie d'un nouveau plan
        :type ajout_plan_date_sortie: int, text
        :param ajout_plan_theme: l'identifiant du thème (qui existe dans la table "Theme") d'un nouveau plan
        :type ajout_plan_theme: int, text
        :param ajout_plan_source: Le lien vers le site officiel Lego
        :type ajout_plan_source: text
        """
        erreurs = []
        if not ajout_plan_id:
            erreurs.append("Veuillez renseigner l'ID du plan.")
        if not ajout_plan_ensemble:
            erreurs.append("Veuillez renseigner le numéro d'ensemble du plan.")
        if not ajout_plan_titre:
            erreurs.append("Veuillez renseigner le titre en français du plan.")
        if not ajout_plan_date_sortie:
            erreurs.append(
                "Veuillez renseigner une l'année de la date de sortie du plan.")
        if not ajout_plan_theme:
            erreurs.append(
                "Veuillez renseigner l'ID du thème du plan")
        if not ajout_plan_source:
            erreurs.append(
                "Veuillez renseigner le type de le lien vers le site Lego")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Plan (champs correspondant aux paramètres du modèle)
        nouveau_plan = Plan(plan_id=ajout_plan_id,
                                  plan_ensemble=ajout_plan_ensemble,
                                  plan_titre=ajout_plan_titre,
                                  plan_date_sortie=ajout_plan_date_sortie,
                                  plan_theme=ajout_plan_theme,
                                  plan_source=ajout_plan_source)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(nouveau_plan)
            db.session.commit()
            return True, nouveau_plan

        except Exception as erreur:
            return False, [str(erreur)]

    # On utilise une méthode statique afin de pouvoir appeler la fonction "supprimer_plan" dans notre fichier generic.py.
    @staticmethod
    def supprimer_plan(plan_id):
        """Fonction qui permet de supprimer un plan dans la BDD
        :param plan_id: l'identifiant du plan
        :type plan_id: int
        :return: True or False et un message d'erreur
        :rtype: booleans, text
        """
        suppr_plan = Plan.query.get(plan_id)

        try:
            db.session.delete(suppr_plan)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]

    # On utilise une méthode statique afin de pouvoir appeler la fonction "association_plan_brique" dans notre fichier generic.py.
    @staticmethod
    def association_plan_brique(plan_id, brique_id):
        """Fonction qui permet d'associer une brique à un plan dans la BDD
        :param brique_id: l'identifiant d'une brique
        :type brique_id: int, text
        :param plan_id: l'identifiant d'un plan
        :type plan_id: int, text
        :return: True or False et un message d'erreur
        :rtype: booleans, text
        """
        erreurs = []
        if not plan_id:
            erreurs.append("Il n'y a pas de plan à associer.")
        if not brique_id:
            erreurs.append("Il n'y a pas brique à associer.")

        # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

        brq = Brique.query.filter(Brique.brique_id == brique_id).first()
        pln = Plan.query.filter(Plan.plan_id == plan_id).first()

        # On vérifier si la brique ou le plan existe dans la base de données.
        if brq is None or pln is None:
            erreurs.append("Le plan ou la brique n'existe pas.")
            return False, erreurs

        # On vérifier si la brique et le plan ne sont pas déjà associés.
        if brq in pln.briques:
            erreurs.append("Le plan ou la brique ou le plan sont déjà associés.")
            return False, erreurs
        else:
            pln.briques.append(brq)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(pln)
            db.session.commit()
            return True, pln

        except Exception as erreur:
            return False, [str(erreur)]

#Table contenant la liste des thèmes des plans
class Theme(db.Model):
    theme_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    theme_nom = db.Column(db.Text, nullable=False)
    plan = db.relationship("Plan", back_populates="theme")
    authorships = db.relationship("Authorship", back_populates="t")

    # On utilise une méthode statique afin de pouvoir appeler la fonction "ajout_theme" dans notre fichier generic.py.
    @staticmethod
    def ajout_theme(ajout_theme_id, ajout_theme_nom):
        """Fonction qui permet d'ajouter un nouveau thème dans la BDD
        :param ajout_theme_id: l'identifiant d'un nouveau thème
        :type ajout_theme_id: int, text
        :param ajout_theme_nom: le nom d'un nouveau thème
        :type ajout_theme_nom: text
        """
        erreurs = []
        if not ajout_theme_id:
            erreurs.append("Veuillez renseigner l'identifiant pour ce thème.")
        if not ajout_theme_nom:
            erreurs.append(
                "Veuillez renseigner le nom du thème.")

            # S'il y a au moins une erreur, afficher un message d'erreur.
        if len(erreurs) > 0:
            return False, erreurs

            # Si aucune erreur n'a été détectée, ajout d'une nouvelle entrée dans la table Theme (champs correspondant aux paramètres du modèle)
        nouveau_theme = Theme(theme_id=ajout_theme_id,
                                      theme_nom=ajout_theme_nom)

        # Tentative d'ajout qui sera stoppée si une erreur apparaît.
        try:
            db.session.add(nouveau_theme)
            db.session.commit()
            return True, nouveau_theme

        except Exception as erreur:
            return False, [str(erreur)]

    # On utilise une méthode statique afin de pouvoir appeler la fonction "supprimer_theme" dans notre fichier generic.py.
    @staticmethod
    def supprimer_theme(theme_id):
        """Fonction qui permet de supprimer un theme dans la BDD
        :param theme_id: l'identifiant d'un thème
        :type theme_id: int
        :return: True or False et un message d'erreur
        :rtype: booleans, text
        """
        suppr_theme = Theme.query.get(theme_id)

        try:
            db.session.delete(suppr_theme)
            db.session.commit()
            return True

        except Exception as erreur:
            return False, [str(erreur)]
