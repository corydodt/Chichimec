 
Nevow.Athena.Widget.subclass(Chichimec, 'RandomNumber').methods(
        function __init__(self, node) {
            Chichimec.RandomNumber.upcall(self, '__init__', node);
            self.filterChanged(12);

            var form = self.node.getElementsByTagName('form')[0];
            form.onsubmit = function () {
                var input = self.node.getElementsByTagName('input')[0];
                var val = input.value;
                self.filterChanged(val);
                return false;
            };
        },

        function number(self, number) {
            var n = self.node.getElementsByTagName('strong')[0];
            n.innerHTML = number;
            return 'ok';
        },

        function filterChanged(self, filter) {
            self.callRemote('setFilter', filter).addCallback(
                function (x) { self.number(x)
            });
        }
);
