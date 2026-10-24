#!/usr/bin/env python3
"""Adversarial intent probes — 20 per supported language, written fresh.

Run: python3 analysis/test_intent.py
Exit code is non-zero if any probe disagrees with the expected label.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))
from audit.intent import DELETE, NON_DELETE, classify  # noqa: E402

EN = [
    ("Please delete my account and everything linked to it.", DELETE),
    ("I want my profile erased permanently.", DELETE),
    ("Close my account; I no longer need it.", DELETE),
    ("Remove all my personal data from your systems.", DELETE),
    ("Delete my account. Actually never mind, keep it.", NON_DELETE),
    ("I don't want my account deleted.", NON_DELETE),
    ("Do not delete anything; I only want a copy.", NON_DELETE),
    ("I need a copy of my invoices, not a deletion.", NON_DELETE),
    ("Please remove me from your mailing list only.", NON_DELETE),
    ("Unsubscribe me from marketing emails.", NON_DELETE),
    ("What happens if I delete my account?", NON_DELETE),
    ("Could you explain how deletion works before I decide?", NON_DELETE),
    ("If you cannot keep my account, delete it.", DELETE),
    ("Delete my account but keep the invoices you must retain.", DELETE),
    ("Delete the search result, not my account.", DELETE),
    ("My account should be gone already; please confirm.", DELETE),
    ("Please confirm that the profile is gone.", DELETE),
    ("I am not asking you to delete my account; fix my address.", NON_DELETE),
    ("Delete everything except billing history.", DELETE),
    ("Stop deleting my saved searches.", NON_DELETE),
]

ES = [
    ("Solicito la eliminación permanente de mi cuenta.", DELETE),
    ("Quiero borrar todos mis datos personales.", DELETE),
    ("Eliminen mi cuenta y la información asociada.", DELETE),
    ("No borren mi cuenta, solo corrijan mi teléfono.", NON_DELETE),
    ("No eliminen nada; necesito una copia.", NON_DELETE),
    ("No quiero que eliminen mi cuenta.", NON_DELETE),
    ("Solo quiero actualizar mi correo, no borrar la cuenta.", NON_DELETE),
    ("Darme de baja de los correos promocionales.", NON_DELETE),
    ("¿Qué pasa si elimino mi cuenta?", NON_DELETE),
    ("Si no pueden conservar la cuenta, elimínenla.", DELETE),
    ("Eliminen la cuenta pero conserven las facturas.", DELETE),
    ("Eliminen el resultado de búsqueda, no mi cuenta.", DELETE),
    ("Mi cuenta ya debería estar borrada; confírmenlo.", DELETE),
    ("Confirma que el perfil ya no existe.", DELETE),
    ("No es una solicitud de borrado, es una corrección.", NON_DELETE),
    ("Borrén la cuenta, por favor.", DELETE),
    ("Necesito una copia de mis datos, sigan con la cuenta activa.", NON_DELETE),
    ("Eliminen todo menos el historial de facturación.", DELETE),
    ("Dejen de eliminar mis búsquedas guardadas.", NON_DELETE),
    ("Quiero cancelar la cuenta definitivamente.", DELETE),
]

PT = [
    ("Solicito a exclusão permanente da minha conta.", DELETE),
    ("Quero apagar todos os meus dados pessoais.", DELETE),
    ("Excluam minha conta e as informações associadas.", DELETE),
    ("Não excluam minha conta, apenas corrijam o telefone.", NON_DELETE),
    ("Não apaguem nada; preciso de uma cópia.", NON_DELETE),
    ("Não quero que excluam minha conta.", NON_DELETE),
    ("Só quero atualizar o e-mail, não apagar a conta.", NON_DELETE),
    ("Quero sair da lista de e-mails promocionais.", NON_DELETE),
    ("O que acontece se eu excluir minha conta?", NON_DELETE),
    ("Se não puderem manter a conta, excluam-na.", DELETE),
    ("Excluam a conta mas mantenham as faturas.", DELETE),
    ("Excluam o resultado da busca, não a conta.", DELETE),
    ("Minha conta já deveria estar apagada; confirmem.", DELETE),
    ("Confirme que o perfil não existe mais.", DELETE),
    ("Não é um pedido de exclusão, é uma correção.", NON_DELETE),
    ("Apaguem a conta, por favor.", DELETE),
    ("Preciso de uma cópia dos dados, mantenham a conta ativa.", NON_DELETE),
    ("Excluam tudo menos o histórico de cobrança.", DELETE),
    ("Parem de excluir minhas buscas salvas.", NON_DELETE),
    ("Quero encerrar a conta definitivamente.", DELETE),
]

FR = [
    ("Je demande la suppression définitive de mon compte.", DELETE),
    ("Je veux effacer toutes mes données personnelles.", DELETE),
    ("Supprimez mon compte et les informations associées.", DELETE),
    ("Ne supprimez pas mon compte, corrigez seulement mon téléphone.", NON_DELETE),
    ("N'effacez rien, j'ai besoin d'une copie.", NON_DELETE),
    ("Je ne veux pas que vous supprimiez mon compte.", NON_DELETE),
    ("Je veux seulement changer d'e-mail, pas supprimer le compte.", NON_DELETE),
    ("Désabonnez-moi des e-mails promotionnels.", NON_DELETE),
    ("Que se passe-t-il si je supprime mon compte ?", NON_DELETE),
    ("Si vous ne pouvez pas garder le compte, supprimez-le.", DELETE),
    ("Supprimez le compte mais gardez les factures.", DELETE),
    ("Supprimez le résultat de recherche, pas mon compte.", DELETE),
    ("Mon compte devrait déjà être supprimé ; confirmez.", DELETE),
    ("Confirmez que le profil n'existe plus.", DELETE),
    ("Ce n'est pas une demande de suppression, c'est une correction.", NON_DELETE),
    ("Supprimez le compte, s'il vous plaît.", DELETE),
    ("J'ai besoin d'une copie, gardez le compte actif.", NON_DELETE),
    ("Supprimez tout sauf l'historique de facturation.", DELETE),
    ("Arrêtez de supprimer mes recherches enregistrées.", NON_DELETE),
    ("Je souhaite fermer définitivement le compte.", DELETE),
]

DE = [
    ("Bitte löschen Sie mein Konto dauerhaft.", DELETE),
    ("Ich möchte alle meine persönlichen Daten löschen lassen.", DELETE),
    ("Löschen Sie mein Konto und die zugehörigen Informationen.", DELETE),
    ("Bitte nicht löschen, korrigieren Sie nur meine Telefonnummer.", NON_DELETE),
    ("Löschen Sie nichts, ich brauche eine Kopie.", NON_DELETE),
    ("Ich möchte nicht, dass mein Konto gelöscht wird.", NON_DELETE),
    ("Ich möchte nur die E-Mail ändern, nicht das Konto löschen.", NON_DELETE),
    ("Melden Sie mich von Werbe-E-Mails ab.", NON_DELETE),
    ("Was passiert, wenn ich mein Konto lösche?", NON_DELETE),
    ("Wenn Sie das Konto nicht behalten können, löschen Sie es.", DELETE),
    ("Löschen Sie das Konto, aber behalten Sie die Rechnungen.", DELETE),
    ("Löschen Sie den Suchtreffer, nicht mein Konto.", DELETE),
    ("Mein Konto sollte schon gelöscht sein; bitte bestätigen.", DELETE),
    ("Bestätigen Sie, dass das Profil nicht mehr existiert.", DELETE),
    ("Das ist keine Löschungsanfrage, sondern eine Korrektur.", NON_DELETE),
    ("Löschen Sie das Konto bitte.", DELETE),
    ("Ich brauche eine Kopie, lassen Sie das Konto aktiv.", NON_DELETE),
    ("Löschen Sie alles außer der Rechnungshistorie.", DELETE),
    ("Hören Sie auf, meine gespeicherten Suchen zu löschen.", NON_DELETE),
    ("Ich möchte das Konto endgültig schließen.", DELETE),
]

KO = [
    ("제 계정을 영구적으로 삭제해 주세요.", DELETE),
    ("모든 개인정보를 삭제하고 싶습니다.", DELETE),
    ("계정과 관련 정보를 삭제해 주세요.", DELETE),
    ("계정을 삭제하지 마세요. 전화번호만 수정해 주세요.", NON_DELETE),
    ("아무것도 삭제하지 마세요. 사본이 필요합니다.", NON_DELETE),
    ("제 계정이 삭제되는 것을 원하지 않습니다.", NON_DELETE),
    ("이메일만 변경하고 싶고 계정은 삭제하지 마세요.", NON_DELETE),
    ("광고 이메일 수신을 중단해 주세요.", NON_DELETE),
    ("계정을 삭제하면 어떻게 되나요?", NON_DELETE),
    ("계정을 유지할 수 없다면 삭제해 주세요.", DELETE),
    ("계정은 삭제하되 청구서는 보관해 주세요.", DELETE),
    ("검색 결과만 삭제하고 계정은 그대로 두세요.", DELETE),
    ("계정이 이미 삭제되었어야 합니다. 확인해 주세요.", DELETE),
    ("프로필이 더 이상 존재하지 않는지 확인해 주세요.", DELETE),
    ("삭제 요청이 아니라 정정 요청입니다.", NON_DELETE),
    ("계정을 삭제해 주세요.", DELETE),
    ("사본이 필요하니 계정은 활성 상태로 두세요.", NON_DELETE),
    ("청구 내역을 제외한 모든 것을 삭제해 주세요.", DELETE),
    ("저장된 검색을 삭제하지 마세요.", NON_DELETE),
    ("계정을 완전히 폐쇄하고 싶습니다.", DELETE),
]

JA = [
    ("アカウントを完全に削除してください。", DELETE),
    ("すべての個人情報を消去したいです。", DELETE),
    ("アカウントと関連情報を削除してください。", DELETE),
    ("アカウントを削除しないでください。電話番号だけ修正してください。", NON_DELETE),
    ("何も削除しないでください。コピーが必要です。", NON_DELETE),
    ("アカウントの削除を希望しません。", NON_DELETE),
    ("メールだけ変更したいので、アカウントは削除しないでください。", NON_DELETE),
    ("広告メールの配信を停止してください。", NON_DELETE),
    ("アカウントを削除するとどうなりますか？", NON_DELETE),
    ("アカウントを維持できない場合は削除してください。", DELETE),
    ("アカウントは削除してください。請求書は保管してください。", DELETE),
    ("検索結果だけ削除してください。アカウントはそのままに。", DELETE),
    ("アカウントはすでに削除されているはずです。確認してください。", DELETE),
    ("プロフィールが存在しないことを確認してください。", DELETE),
    ("削除依頼ではなく訂正依頼です。", NON_DELETE),
    ("アカウントを削除してください。", DELETE),
    ("コピーが必要なので、アカウントは有効なままにしてください。", NON_DELETE),
    ("請求履歴以外のすべてを削除してください。", DELETE),
    ("保存した検索を削除しないでください。", NON_DELETE),
    ("アカウントを完全に閉鎖したいです。", DELETE),
]

ALL = {"en": EN, "es": ES, "pt": PT, "fr": FR, "de": DE, "ko": KO, "ja": JA}


def main() -> int:
    total = failures = 0
    for lang, probes in ALL.items():
        bad = []
        for text, want in probes:
            total += 1
            got, why = classify(text)
            if got != want:
                failures += 1
                bad.append((text, want, got, why))
        print(f"{lang}: {len(probes) - len(bad)}/{len(probes)}")
        for text, want, got, why in bad:
            print(f"   FAIL want={want} got={got} ({why}) :: {text}")
    print(f"\n{total - failures}/{total} probes pass")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
