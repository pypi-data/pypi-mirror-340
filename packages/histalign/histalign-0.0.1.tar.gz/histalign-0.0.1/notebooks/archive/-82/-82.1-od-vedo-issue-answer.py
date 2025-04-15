from vedo import *

# settings.default_backend = "vtk"

normal = [0, 0, 1]
cmap = "gist_stern_r"


def func(w, _):
    c, n = pcutter.origin, pcutter.normal
    vslice = vol.slice_plane(c, n, autocrop=True).cmap(cmap)
    vslice.name = "Slice"
    plt.at(1).remove("Slice").add(vslice)


def keypress(event):
    if event.keypress == "q":
        plt.close()
        return
    if event.keypress == "s":
        print("Plane origin:", pcutter.origin, "normal:", pcutter.normal)


vol = Volume(dataurl + "embryo.slc").cmap(cmap)
vslice = vol.slice_plane(vol.center(), normal).cmap(cmap)
vslice.name = "Slice"

settings.enable_default_keyboard_callbacks = False

plt = Plotter(axes=0, N=2, bg="k", bg2="bb", interactive=False)
plt.add_callback("keypress", keypress)

pcutter = PlaneCutter(
    vslice,
    normal=normal,
    alpha=0,
    c="white",
    padding=0,
    can_translate=False,
    can_scale=False,
)
pcutter.add_observer("interaction", func)
plt.at(0).show(vol, zoom=1.5)
plt.at(1).add(pcutter)
plt.interactive()
plt.close()
