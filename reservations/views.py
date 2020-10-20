from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.

from uuid import UUID

from django.shortcuts import render, redirect, get_object_or_404

from .forms import ReservationCreateForm, ReservationUpdateForm
from .models import Reservation
from .reservations import create_new_reservation, get_reservation_list, update_existing_reservation, delete_existing_reservation


def reservations(request):
    """

    :param request:
    :return:
    """
    reservations = get_reservation_list(request)
    return render(request, 'reservations.html', {'reservations': reservations})


def reservation_create(request):
    """

    :param request:
    :return:
    """
    if request.method == "POST":
        form = reservationCreateForm(request.POST)
        if form.is_valid():
            reservation_uuid = create_new_reservation(request, form)
            return redirect('reservation_detail', reservation_uuid=reservation_uuid)
    else:
        form = reservationCreateForm()
    return render(request, 'reservation_create.html', {'form': form})


def reservation_detail(request, reservation_uuid):
    """

    :param request:
    :param project_uuid:
    :return:
    """
    reservation = get_object_or_404(reservation, uuid=UUID(str(reservation_uuid)))
    reservation_reservations = reservation.reservation_reservations.order_by('name')
    return render(request, 'reservation_detail.html', {'reservation': reservation, 'reservation_members': reservation_members})


def reservation_update(request, reservation_uuid):
    """

    :param request:
    :param reservation_uuid:
    :return:
    """
    reservation = get_object_or_404(reservation, uuid=UUID(str(reservation_uuid)))
    if request.method == "POST":
        form = reservationUpdateForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation_uuid = update_existing_reservation(request, reservation, form)
            return redirect('reservation_detail', reservation_uuid=str(reservation.uuid))
    else:
        form = reservationUpdateForm(instance=reservation)
    return render(request, 'reservation_update.html',
                  {
                      'form': form, 'project_uuid': str(reservation_uuid), 'reservation_name': reservation.name}
                  )


def reservation_delete(request, reservation_uuid):
    """

    :param request:
    :param reservation_uuid:
    :return:
    """
    reservation = get_object_or_404(Project, uuid=UUID(str(project_uuid)))
    reservation_members = reservation.reservation_reservations.order_by('name')
    if request.method == "POST":
        is_removed = delete_existing_reservation(request, reservation)
        if is_removed:
            return redirect('reservations')
    return render(request, 'reservation_delete.html', {'reservation': reservation, 'reservation_reservations': reservation_reservations})
