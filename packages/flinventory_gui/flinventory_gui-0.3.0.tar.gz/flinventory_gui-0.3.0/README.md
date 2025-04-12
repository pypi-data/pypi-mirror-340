# flinventory GUI

![Search screenshot](docs/screenshot_search.png)

A GUI for the flinventory project/ data format.

## Run

Getting code:
`git clone https://codeberg.org/flukx/flinventory-gui.git`

Getting prerequisites:
- Getting flinventory, which is not published as a package yet:
- ```commandline
  git clone https://codeberg.org/flukx/flinventory.git
  cd flinventory
  nix-shell  # or install pdm your way
  pdm build
```
Then use the way you prefer:
- ```commandline
  conda create -f environment.yml`
  conda activate bikeparts-gui
  pip install flinventory/dist/dist/flinventory-0.1.1-py3-none-any.whl
  ```
- or virtualenv:
  ```commandline
  python -m venv .venv
  source .venv/bin/activate
  pip install -r nicegui flinventory/dist/dist/flinventory-0.1.1-py3-none-any.whl
  ```
- or nix-shell (unfortunately no working setup found. Please help!)

Getting data: `git clone -b harzgerode-main https://codeberg.org/flukx/flings.git`
Run it:
```commandline
python flinventory_gui/search.py flings
```
It should open a browser with the search page. Otherwise, open [localhost:11111](http://localhost:11111)
in your browser.

To see all options run `python flinventory_gui/search.py --help` but note that many of them are inherited
from the underlying module `flinventory` and are not used.

### Build and install with pip
Building `flinventory_gui`:
`pdm build`
and install in a venv:
  ```commandline
  python -m venv .venv
  source .venv/bin/activate
  pip install dist/....whl
  ```
But currently it is supported to actually run this installed package.

## Making website accessible in local network

It's nice to use the thing search on the computer where it is run but often it's more helpful to
use it on other mobile devices. Therefore, you can make the search page available in the local network
by opening the port (by default `11111` in the firewall.)

In Fedora KDE I opened "Firewall" and in the Configuration "Runtime" in Tab "Zones" in zone "public" in tab "Ports"
added `11111` for protocol `tcp`.

In NixOS KDE I typed ([for temporary access](https://discourse.nixos.org/t/how-to-temporarily-open-a-tcp-port-in-nixos/12306/10)):
```commandline
sudo iptables -A INPUT -p tcp --dport 11111 -j ACCEPT
sudo systemctl reload firewall
```
For permanent usage, use the `configuration.nix` with the line
`networking.firewall.allowedTCPPorts = [ 11111 ];`.

## Ideas for the future

- Somehow really make the search async. Since filtering the correct parts and displaying them
  has no waiting periods (with `await`) it cannot really be cancelled.
  - Also helpful: show only 10 best results.
- Add filter for search that shows a bike where you can click on parts. And then only parts that are
  "part_of" this are shown. When clicked on the brakes, it shows a list of brake types (sub categories)
  that you can click on again. [Interactive image](https://nicegui.io/documentation/interactive_image)
  could be helpful.
  - Make this filter keyboard accessible. Ctrl+F activates choice, then letter chooses something which is
    marked in the text on the bike picture.
- Figure out why sometimes the page reloads completely.
