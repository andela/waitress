from rest_framework import serializers
from app.models import CountTrue


class UserSerializer(serializers.Serializer):
    """
    A serializer class for serializing the SlackUsers
    """

    id = serializers.IntegerField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    photo = serializers.CharField()
    is_active = serializers.BooleanField()
    is_tapped = serializers.BooleanField()


class SecureUserSerializer(UserSerializer):
    """
    A serializer class for serializing SlackUsers that exposes the SlackID.

    This is used only under authorized access.
    """

    slack_id = serializers.CharField()


class FilterSerializer(serializers.Serializer):
    filter = serializers.CharField()


# class PassPhraseSerializer(serializers.Serializer):
#     passphrase = serializers.CharField()


class AddUserSerializer(serializers.Serializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    utype = serializers.CharField()
    passphrase = serializers.CharField()


class ReportSerializer(serializers.Serializer):
    @classmethod
    def count(cls, queryset):
        """
        This method counts the number of breakfast and lunch served.

        It writes the results to a list having the below structure.
            [
                {breakfast:XX, lunch:XX, date:"YYYY-MM-DD"},
                ..
            ]
        """
        result_group = queryset.values("date")
        annotate_report = result_group.annotate(
            breakfast=CountTrue("breakfast"), lunch=CountTrue("lunch")
        )

        def serialize(queryset):
            return [
                {
                    "breakfast": res["breakfast"],
                    "lunch": res["lunch"],
                    "date": res["date"],
                }
                for res in queryset
            ]

        return serialize(annotate_report)
        # lunch = queryset.filter(lunch=1).values('date').count()
