from django.test import TestCase, Client
from django.contrib.auth.models import User
from fichas.models import Membro, Ingrediente, Ficha, Chave
from django.urls import reverse
import copy
from django.template.context import BaseContext, Context

# Patch for Python 3.14 compatibility with Django 4.2 Test Client template context copying
def _patched_base_context_copy(self):
    cls = self.__class__
    duplicate = cls.__new__(cls)
    for k, v in self.__dict__.items():
        setattr(duplicate, k, v)
    duplicate.dicts = self.dicts[:]
    return duplicate

def _patched_context_copy(self):
    duplicate = _patched_base_context_copy(self)
    duplicate.render_context = copy.copy(self.render_context)
    return duplicate

BaseContext.__copy__ = _patched_base_context_copy
Context.__copy__ = _patched_context_copy


class MemberManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create admin user
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        self.admin_membro = Membro.objects.create(usuario=self.admin_user, nome='admin', semestre='2020/1', email='admin@nutrijr.com')
        
        # Create regular members
        self.user1 = User.objects.create_user(username='membro1', password='password123')
        self.membro1 = Membro.objects.create(usuario=self.user1, nome='Membro 1', semestre='2021/1', email='membro1@nutrijr.com')
        
        self.user2 = User.objects.create_user(username='membro2', password='password123')
        self.membro2 = Membro.objects.create(usuario=self.user2, nome='Membro 2', semestre='2021/2', email='membro2@nutrijr.com')
        
        # Create key
        self.chave = Chave.objects.create(key='secret123')
        
        # Create some items authored by membro1
        self.ingrediente = Ingrediente.objects.create(
            autorIng=self.membro1,
            nomeIng='Farinha',
            origemDosDados='TACO'
        )
        self.ficha = Ficha.objects.create(
            autor=self.membro1,
            nomeFicha='Bolo de Cenoura',
            cliente='Cliente Teste'
        )

    def test_deleta_membro_success(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('deletaMembro'), {
            'membroExcluido': self.membro1.pk,
            'membroDestino': self.membro2.pk,
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn('Transferidos', json_data['ajax_message'])
        
        # Verify membro1 and user1 are deleted
        self.assertFalse(User.objects.filter(username='membro1').exists())
        self.assertFalse(Membro.objects.filter(pk=self.membro1.pk).exists())
        
        # Verify authorship was transferred to membro2
        self.ingrediente.refresh_from_db()
        self.ficha.refresh_from_db()
        self.assertEqual(self.ingrediente.autorIng, self.membro2)
        self.assertEqual(self.ficha.autor, self.membro2)

    def test_deleta_membro_same_source_and_dest(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('deletaMembro'), {
            'membroExcluido': self.membro1.pk,
            'membroDestino': self.membro1.pk,
        })
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertIn('form_errors', json_data)
        self.assertIn('distintos', json_data['form_errors'])
        
        # Verify membro1 was not deleted
        self.assertTrue(Membro.objects.filter(pk=self.membro1.pk).exists())

    def test_deleta_membro_cannot_delete_admin(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('deletaMembro'), {
            'membroExcluido': self.admin_membro.pk,
            'membroDestino': self.membro2.pk,
        })
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertIn('admin não pode ser excluído', json_data['ajax_message'])
        self.assertTrue(User.objects.filter(username='admin').exists())

    def test_deleta_membro_non_admin_forbidden(self):
        self.client.login(username='membro1', password='password123')
        response = self.client.post(reverse('deletaMembro'), {
            'membroExcluido': self.membro2.pk,
            'membroDestino': self.membro1.pk,
        })
        self.assertEqual(response.status_code, 403)

    def test_muda_chave_success(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('mudaChave'), {
            'key': 'newkey456'
        })
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertEqual(json_data['nova_chave'], 'newkey456')
        self.assertEqual(Chave.objects.last().key, 'newkey456')

    def test_troca_senha_success(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('trocaSenha'), {
            'usuario': self.user1.pk,
            'nova_senha': 'newpassword789'
        })
        self.assertEqual(response.status_code, 200)
        
        # Test logging in with new password
        login_success = self.client.login(username='membro1', password='newpassword789')
        self.assertTrue(login_success)

    def test_lista_membros_admin_view(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('listaMembros'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['eh_admin'])
        self.assertContains(response, 'Excluir Membro')
        self.assertContains(response, 'Definir nova chave')
        self.assertContains(response, 'Alterar senhas')

    def test_lista_membros_regular_user_view(self):
        self.client.login(username='membro1', password='password123')
        response = self.client.get(reverse('listaMembros'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['eh_admin'])
        self.assertNotContains(response, 'id="apaga_membro_form"')

    def test_registrar_membro_success(self):
        response = self.client.post(reverse('registrarMembro'), {
            'nome': 'Novo Membro',
            'semestre': '2022/1',
            'email': 'novo@nutrijr.com',
            'senha1': 'novasenha123',
            'senha2': 'novasenha123',
            'chave': 'secret123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='Novo Membro').exists())
        self.assertTrue(Membro.objects.filter(nome='Novo Membro').exists())

    def test_registrar_membro_wrong_key(self):
        response = self.client.post(reverse('registrarMembro'), {
            'nome': 'Membro Errado',
            'semestre': '2022/1',
            'email': 'errado@nutrijr.com',
            'senha1': 'novasenha123',
            'senha2': 'novasenha123',
            'chave': 'chave_errada',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='Membro Errado').exists())

    def test_lista_fichas_and_ingredientes(self):
        self.client.login(username='membro1', password='password123')
        
        # Test listaFichas
        response_fichas = self.client.get(reverse('listaFichas'))
        self.assertEqual(response_fichas.status_code, 200)
        self.assertContains(response_fichas, 'Bolo de Cenoura')
        
        # Test listaIngredientes
        response_ing = self.client.get(reverse('listaIngredientes'))
        self.assertEqual(response_ing.status_code, 200)
        self.assertContains(response_ing, 'Farinha')

