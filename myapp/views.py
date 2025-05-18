from datetime import timezone

from django.contrib.humanize.templatetags.humanize import intcomma
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import ThucDon, DonHang, ChiTietDonHang
from django.contrib import messages
from decimal import Decimal
@login_required
def menu_management(request):
    if request.user.vai_tro != 'quan_ly':
        return HttpResponse("Bạn không có quyền truy cập trang này.", status=403)

    thuc_don = ThucDon.objects.all()
    return render(request, 'menu_quanly.html', {'thuc_don': thuc_don})

@login_required
def redirect_based_on_role(request):
    if request.user.vai_tro == 'quan_ly':
        return redirect('menu_management')
    elif request.user.vai_tro == 'nhan_vien':
        return redirect('menu_nhanvien')
    elif request.user.vai_tro == 'khach_hang':
        return redirect('menu_khachhang')
    else:
        return redirect('logout')

@login_required
def add_menu_item(request):
    if request.user.vai_tro != 'quan_ly':
        return HttpResponse("Bạn không có quyền truy cập.", status=403)

    if request.method == "POST":
        ten_mon = request.POST.get('ten_mon')
        gia_tien = request.POST.get('gia_tien')
        hinh_anh = request.FILES.get('hinh_anh')

        try:
            mon = ThucDon(ten_mon=ten_mon, gia_tien=gia_tien, hinh_anh=hinh_anh)
            mon.save()
            messages.success(request, "Thêm món thành công!")
        except Exception as e:
            messages.error(request, f"Lỗi khi thêm món: {str(e)}")

        return redirect('menu_management')
    return redirect('menu_management')

@login_required
def edit_menu_item(request):
    if request.user.vai_tro != 'quan_ly':
        return HttpResponse("Bạn không có quyền truy cập.", status=403)

    if request.method == "POST":
        ma_mon = request.POST.get('ma_mon')
        mon = get_object_or_404(ThucDon, ma_mon=ma_mon)

        mon.ten_mon = request.POST.get('ten_mon')
        mon.gia_tien = request.POST.get('gia_tien')
        if request.FILES.get('hinh_anh'):
            mon.hinh_anh = request.FILES.get('hinh_anh')

        try:
            mon.save()
            messages.success(request, "Sửa món thành công!")
        except Exception as e:
            messages.error(request, f"Lỗi khi sửa món: {str(e)}")

        return redirect('menu_management')
    return redirect('menu_management')

@login_required
def toggle_menu_item_visibility(request):
    if request.user.vai_tro != 'quan_ly':
        return HttpResponse("Bạn không có quyền truy cập.", status=403)

    if request.method == "POST":
        ma_mon = request.POST.get('ma_mon')
        da_an = request.POST.get('da_an') == 'true'
        mon = get_object_or_404(ThucDon, ma_mon=ma_mon)

        try:
            mon.da_an = da_an
            mon.save()
            action = "Ẩn" if da_an else "Hiện"
            messages.success(request, f"{action} món thành công!")
        except Exception as e:
            messages.error(request, f"Lỗi khi {action.lower()} món: {str(e)}")

    return redirect('myapp:menu_management')

@login_required
def menu_nhanvien(request):
    if request.user.vai_tro != 'nhan_vien':
        return HttpResponse("Bạn không có quyền truy cập trang này.", status=403)

    thuc_don = ThucDon.objects.all()
    return render(request, 'menu_nhanvien.html', {'thuc_don': thuc_don})

@login_required
def edit_menu_item_nhanvien(request):
    if request.user.vai_tro != 'nhan_vien':
        return HttpResponse("Bạn không có quyền truy cập.", status=403)

    if request.method == "POST":
        ma_mon = request.POST.get('ma_mon')
        mon = get_object_or_404(ThucDon, ma_mon=ma_mon)

        mon.ten_mon = request.POST.get('ten_mon')
        mon.gia_tien = request.POST.get('gia_tien')
        if request.FILES.get('hinh_anh'):
            mon.hinh_anh = request.FILES.get('hinh_anh')

        try:
            mon.save()
            messages.success(request, "Sửa món thành công!")
        except Exception as e:
            messages.error(request, f"Lỗi khi sửa món: {str(e)}")

        return redirect('menu_nhanvien')
    return redirect('menu_nhanvien')

@login_required
def toggle_menu_item_visibility_nhanvien(request):
    if request.user.vai_tro != 'nhan_vien':
        return HttpResponse("Bạn không có quyền truy cập.", status=403)

    if request.method == "POST":
        ma_mon = request.POST.get('ma_mon')
        da_an = request.POST.get('da_an') == 'true'
        mon = get_object_or_404(ThucDon, ma_mon=ma_mon)

        try:
            mon.da_an = da_an
            mon.save()
            action = "Ẩn" if da_an else "Hiện"
            messages.success(request, f"{action} món thành công!")
        except Exception as e:
            messages.error(request, f"Lỗi khi {action.lower()} món: {str(e)}")

    return redirect('menu_nhanvien')

@login_required
def menu_khachhang(request):
    if request.user.vai_tro != 'khach_hang':
        return HttpResponse("Bạn không có quyền truy cập trang này.", status=403)

    thuc_don = ThucDon.objects.filter(da_an=False)  # Chỉ hiển thị món không ẩn
    return render(request, 'menu_khachhang.html', {'thuc_don': thuc_don})

@login_required
def add_to_cart(request):
    if request.user.vai_tro != 'khach_hang':
        return HttpResponse("Bạn không có quyền truy cập.", status=403)

    if request.method == "POST":
        ma_mon = request.POST.get('ma_mon')
        so_luong = int(request.POST.get('so_luong', 1))
        mon = get_object_or_404(ThucDon, ma_mon=ma_mon)

        don_hang, created = DonHang.objects.get_or_create(
            nguoi_dung=request.user,
            trang_thai='cho_xac_nhan',
            loai_don_hang='truc_tuyen',
            defaults={'tong_tien': 0}
        )

        chi_tiet, chi_tiet_created = ChiTietDonHang.objects.get_or_create(
            don_hang=don_hang,
            mon_an=mon,
            defaults={'so_luong': so_luong, 'gia_tien': mon.gia_tien}
        )

        if not chi_tiet_created:
            chi_tiet.so_luong += so_luong
            chi_tiet.save()

        don_hang.tong_tien += mon.gia_tien * so_luong
        don_hang.save()

        messages.success(request, f"Đã thêm {mon.ten_mon} vào giỏ hàng!")
        return redirect('menu_khachhang')

    return redirect('menu_khachhang')


def order_list(request):
    # Lấy tất cả đơn hàng
    don_hang_list = DonHang.objects.all().order_by('-ngay_tao')

    # Lấy tất cả món ăn
    thuc_don = ThucDon.objects.all()

    # Các lựa chọn cho dropdown
    loai_don_hang_choices = DonHang.LOAI_DON_HANG
    trang_thai_choices = DonHang.TRANG_THAI
    thanh_toan_choices = DonHang.THANH_TOAN

    context = {
        'don_hang_list': don_hang_list,
        'thuc_don': thuc_don,
        'loai_don_hang_choices': loai_don_hang_choices,
        'trang_thai_choices': trang_thai_choices,
        'thanh_toan_choices': thanh_toan_choices,

        'intcomma': intcomma,  # Dùng để định dạng số trong template
    }
    return render(request, 'quanlydonhang_ql.html', context)


from django.contrib.auth.decorators import login_required


@login_required
def create_order(request):
    if request.method == 'POST':
        try:
            # Lấy tên khách hàng từ người dùng đăng nhập nếu không có trong form
            ten_khach_hang = request.POST.get('ten_khach_hang') or request.user.ho_ten or request.user.username
            loai_don_hang = request.POST.get('loai_don_hang')
            trang_thai = request.POST.get('trang_thai')
            thanh_toan = request.POST.get('thanh_toan')
            dia_chi = request.POST.get('dia_chi', '')
            ngay_tao = request.POST.get('ngay_tao')

            total_money = Decimal(0)
            order_details = []
            thuc_don = ThucDon.objects.all()

            for mon in thuc_don:
                checkbox = request.POST.get(f'mon_an_{mon.ma_mon}')
                quantity = request.POST.get(f'so_luong_{mon.ma_mon}', '0')
                if checkbox and int(quantity) > 0:
                    quantity = int(quantity)
                    subtotal = mon.gia_tien * quantity
                    total_money += subtotal
                    order_details.append({
                        'mon_an': mon,
                        'so_luong': quantity,
                        'gia_tien': mon.gia_tien,
                    })

            if total_money == 0:
                messages.error(request, 'Vui lòng chọn ít nhất một món ăn với số lượng lớn hơn 0.')
                return redirect('myapp:order_list')

            don_hang = DonHang.objects.create(
                ten_khach_hang=ten_khach_hang,
                loai_don_hang=loai_don_hang,
                trang_thai=trang_thai,
                thanh_toan=thanh_toan,
                dia_chi=dia_chi if loai_don_hang == 'truc_tuyen' else '',
                ngay_tao=ngay_tao,
                tong_tien=total_money,
            )

            for detail in order_details:
                ChiTietDonHang.objects.create(
                    don_hang=don_hang,
                    mon_an=detail['mon_an'],
                    so_luong=detail['so_luong'],
                    gia_tien=detail['gia_tien'],
                )

            messages.success(request, f'Đơn hàng {don_hang.ma_don_hang} đã được tạo thành công.')
            return redirect('myapp:order_list')

        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            return redirect('myapp:order_list')

    return redirect('myapp:order_list')


@login_required
def update_order_status(request):
    if request.method == 'POST':
        ma_don_hang = request.POST.get('ma_don_hang')
        trang_thai = request.POST.get('trang_thai')

        try:
            don_hang = get_object_or_404(DonHang, ma_don_hang=ma_don_hang)
            if trang_thai in dict(DonHang.TRANG_THAI).keys():
                don_hang.trang_thai = trang_thai
                don_hang.save()
                messages.success(request, 'Cập nhật trạng thái thành công!')
            else:
                messages.error(request, 'Trạng thái không hợp lệ!')
        except Exception as e:
            messages.error(request, f'Lỗi khi cập nhật trạng thái: {str(e)}')

        return redirect('myapp:order_list')

    return redirect('myapp:order_list')