from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ai.services.analysis_service import generate_analysis_for_user


class Command(BaseCommand):
    help = 'Executa analise financeira com IA para usuarios ativos do sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email do usuario para analise especifica',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Executa analise para todos os usuarios ativos',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        user_email = options.get('user_email')
        run_all = options.get('all')

        if user_email:
            users = User.objects.filter(email=user_email, is_active=True)
            if not users.exists():
                self.stdout.write(self.style.ERROR(
                    f'Usuario com email "{user_email}" nao encontrado ou inativo.'
                ))
                return
        elif run_all:
            users = User.objects.filter(is_active=True)
            self.stdout.write(f'Analisando todos os {users.count()} usuarios ativos...')
        else:
            self.stdout.write(self.style.WARNING(
                'Use --user-email <email> para um usuario especifico ou --all para todos.'
            ))
            self.stdout.write('Exemplo: python manage.py run_finance_analysis --all')
            return

        success_count = 0
        error_count = 0

        for user in users:
            self.stdout.write(f'Analisando usuario ID {user.id}...')
            try:
                analysis = generate_analysis_for_user(user.id)
                success_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Analise ID {analysis.id} concluida para usuario ID {user.id}'
                ))
            except ValueError as e:
                error_count += 1
                self.stdout.write(self.style.WARNING(
                    f'Usuario ID {user.id}: {str(e)}'
                ))
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(
                    f'Erro ao analisar usuario ID {user.id}: {str(e)}'
                ))

        total = success_count + error_count
        self.stdout.write('---')
        self.stdout.write(
            self.style.SUCCESS(f'Total: {total} | Sucesso: {success_count} | Erros: {error_count}')
        )
