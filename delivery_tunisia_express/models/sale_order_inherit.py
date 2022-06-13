from odoo import _, fields, models, api
import requests
from datetime import date
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    user_name = fields.Char(string="Login Tunisia", related="carrier_id.user_name")
    destinataire = fields.Char(string="Name of Receiver", related="carrier_id.destinataire")
    adresse_de_livraison = fields.Char(string="Delivery City")
    gouvernorat_livraison = fields.Integer(string="Delivery Department Code")
    telephone_de_contact_livraison = fields.Char(string="Receiver Contact No")
    code_postal_livraison = fields.Integer(string="Postcode Delivery City")
    date_enlevement = fields.Date(string="Expected Date of Pickup")
    date_livraison = fields.Date(string="Expected Date of Delivery")
    nombre_de_colis = fields.Integer(string="Number of Package")
    libelle_de_marchandise = fields.Char(string="Description of Delivered Item")
    valeur_marchandise = fields.Float(string="COD")
    barcode_client = fields.Char(string="Barcode")
    description = fields.Char(string="Additional Information")
    adresse_enlevement = fields.Char(string="Vendor City")
    gouvernorat_enlevement = fields.Integer(string="Delivery Department Code")
    code_postal_enlevement = fields.Integer(string="Postcode Delivery City")
    telephone_de_contact_enlevement = fields.Integer(string="Item Receiver Telephone")
    id_commande_client = fields.Char(string="Vendor Name")
    shipment_confirm_chk = fields.Boolean()

    carrier_id_new = fields.Char('Carrier', related="carrier_id.name")

    def shipment_confirm(self):
        if not self.user_name:
            raise ValidationError(_("You can't request an shipment order! Please provide Login Tunisia"))
        if not self.destinataire:
            raise ValidationError(_("You can't request an shipment order! Please provide Name of Reciever"))
        if not self.date_enlevement:
            raise ValidationError(_("You can't request an shipment order! Please provide Expected Date of Pickup"))
        if not self.date_livraison:
            raise ValidationError(_("You can't request an shipment order! Please provide Expected Date of Delivery"))
        if not self.adresse_de_livraison:
            raise ValidationError(_("You can't request an shipment order! Please provide Delivery City"))
        if not self.gouvernorat_livraison:
            raise ValidationError(_("You can't request an shipment order! Please provide Delivery Department Code"))
        if not self.telephone_de_contact_livraison:
            raise ValidationError(_("You can't request an shipment order! Please provide Reciever Contact No"))
        if not self.code_postal_livraison:
            raise ValidationError(_("You can't request an shipment order! Please provide Post Code Delivery City"))
        if not self.nombre_de_colis:
            raise ValidationError(_("You can't request an shipment order! Please provide Number of Package"))
        if not self.libelle_de_marchandise:
            raise ValidationError(_("You can't request an shipment order! Please provide Description of Delivered Items"))
        if not self.valeur_marchandise:
            raise ValidationError(_("You can't request an shipment order! Please provide COD"))
        if not self.barcode_client:
            raise ValidationError(_("You can't request an shipment order! Please provide Barcode"))
        date_enlevement = self.date_enlevement.strftime('%YYYY-%MM-%DD')
        date_livraison = self.date_livraison.strftime('%YYYY-%MM-%DD')
        res = requests.get(url='http://pro.tunisia-express.tn/api/floraisontunisie/additem?format=json&api_key='+self.user_name+'&destinataire='+str(self.destinataire)+'&user_name='+str(self.destinataire)+'&date_enlevement='+str(date_enlevement)+'&date_livraison='+str(date_livraison)+'&adresse_de_livraison='+str(self.adresse_de_livraison)+'&gouvernorat_livraison='+str(self.gouvernorat_livraison)+'&telephone_de_contact_livraison='+str(self.telephone_de_contact_livraison)+'&code_postal_livraison='+str(self.code_postal_livraison)+'&nombre_de_colis='+str(self.nombre_de_colis)+'&libelle_de_marchandise='+str(self.libelle_de_marchandise)+'&valeur_marchandise='+str(self.valeur_marchandise)+'&barcode_client='+str(self.barcode_client)+'')
        if res.status_code == 200:
            self.shipment_confirm_chk = True
            message_id = self.env['mymodule.message.wizard'].create({'barcode': self.barcode_client, 'message': "Your Item Has Been Created"})
            return {
                'name': 'Successfull',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        else:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Oups! Vous devez renseigner un destinataire valide!"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }

    def barcode_track(self):
        res = requests.get('http://pro.tunisia-express.tn/api/example/tracking/barcode/'+self.barcode_client+'/api_key/'+self.user_name+'/format/json')
        if res.status_code == 404:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Tracking Items Could Not be Found"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 100:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "En attente! Colis pas encore enlevé"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 101:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "enlevé! enlèvement effectue"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 102:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Dans le dépôt! colis dans le dépôt"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 103:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Livraison en cours! Colis en cours de livraison"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 104:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Livré! Livraison effectuée"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 115:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Livraison reportée- numéro erroné! Livraison annulée, retour au dépôt. Motif: Numéro du client erroné"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 125:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Livraison reportee - client injoignable! Livraison annulée, retour au dépôt. Motif: Client injoignable"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 135:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Livraison reportée - client non dispo!Livraison annulée, retour au dépôt. Motif: Client non disponible"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 116:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Retour à l'expéditeur! Retour à l'expéditeur."})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        if res.status_code == 126:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Annulé - Commande erronée! Livraison annulée, retour à l'expéditeur. Motif: Commande erronée"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 136:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Annulé - Client non sérieux! Livraison annulée, retour à l'expéditeur. Motif: Client non sérieux"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 140:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Rendez-vous planifié! Rendez-vous planifié"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 145:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Livraison reportée - adresse de livraison erronée! Livraison annulée. retour au dépôt. Motif: adresse de livraison erronée"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 146:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Encours de préparation - Retour à l’expéditeur! Encours de préparation - Retour à l’expéditeur"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 147:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Livraison reportée, Motif: Client ne décroche pas! Livraison reportée, Motif: Client ne décroche pas le Tel"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 150:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis égaré! Colis égaré"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 501:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis en transition vers Jendouba! Colis en transition vers Jendouba"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 502:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis en transition vers Sousse! Colis en transition vers Sousse"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 503:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis en transition vers Gafsa! Colis en transition vers Gafsa"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 504:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis en transition vers Sfax! Colis en transition vers Sfax"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 505:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis en transition vers Mednine! Colis en transition vers Mednine"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 506:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis en transition vers Tunis! Colis en transition vers Tunis"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 511:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis reçu à Jendouba! Colis reçu à Jendouba"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 512:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis reçu à Sousse! Colis reçu à Sousse"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 513:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis reçu à Gafsa! Colis reçu à Gafsa"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 514:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis reçu à Sfax! Colis reçu à Sfax"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 515:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis reçu à Mednine! Colis reçu à Mednine"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 100:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "En attente! Colis pas encore enlevé"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 516:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "Colis reçu à Tunis! Colis reçu à Tunis"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 100:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "En attente! Colis pas encore enlevé"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }
        elif res.status_code == 100:
            message_id = self.env['mymodule.message.wizard.error'].create(
                {'message': "En attente! Colis pas encore enlevé"})
            return {
                'name': 'Error',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mymodule.message.wizard.error',
                # pass the id
                'res_id': message_id.id,
                'target': 'new'
            }

class MyModuleMessageWizard(models.TransientModel):
    _name = 'mymodule.message.wizard'
    _description = "Show Message"

    message = fields.Text('Message')
    barcode = fields.Text('Message')

    @api.model
    def action_close(self, vals):
        return {'type': 'ir.actions.act_window_close'}


class MyModuleMessageWizard1(models.TransientModel):
    _name = 'mymodule.message.wizard.error'
    _description = "Show Message"

    message = fields.Text('Message')

    @api.model
    def action_close_2(self, vals):
        return {'type': 'ir.actions.act_window_close'}
