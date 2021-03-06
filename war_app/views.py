import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/fight/'+request.POST['number'])
        # return render(request, 'fight.html', {'range': range(1, int(request.POST['number']) + 1)})
    return render(request, 'index.html')

class Warrior:
    health = 100

    def attack(self, enemy):
        damage = random.randint(0, 30)
        enemy.health = (enemy.health - damage) if (enemy.health - damage) >= 0 else 0
        return damage


def fight(request, number):
    if request.method == 'POST':
        warriors_name = request.POST.getlist('w')
        war_participents = []
        res = []

        for w in warriors_name:
            warrior = Warrior()
            warrior.name = w
            war_participents.append(warrior)

        # while all(i['health'] > 0 for i in war_participents):
        while len(war_participents) > 1:
            attacker = random.choice(war_participents)
            war_participents.remove(attacker)
            defender = random.choice(war_participents)
            war_participents.append(attacker)
            damage = attacker.attack(defender)
            res.append(attacker.name + ' attacked. ' +
                       defender.name + ' lost ' + str(damage) + ' points. ' + str(defender.health) + ' points left.')
            if defender.health is 0:
                war_participents.remove(defender)
                res.append(defender.name + ' was killed by ' + attacker.name + '.')

        winner = war_participents[0].name
        return render(request, 'result.html', {
            'winner': winner,
            'process': res
        })
    else:
        return render(request, 'fight.html', {'range': range(1, int(number) + 1)})

def fight2(request):
    if request.method == 'POST':
        w1, w2 = Warrior(), Warrior()
        w1.name = request.POST['w1']
        w2.name = request.POST['w2']
        war_participents = (w1, w2)
        res = []
        while w1.health > 0 and w2.health > 0:
            attacker = random.choice(war_participents)
            defender = w1 if attacker is w2 else w2
            damage = attacker.attack(defender)
            res.append(attacker.name + ' attacked. ' +
                       defender.name + ' lost ' + str(damage) + ' points. ' + str(defender.health) + ' points left.')

        winner = w1.name if w2.health is 0 else w2.name
        return render(request, 'result.html', {
            'winner': winner,
            'process': res
        })
    else:
        return render(request, 'fight.html')


def war(request):
    if request.method == 'POST':
        w1, w2 = Warrior(), Warrior()
        w1.name = request.POST['w1']
        w2.name = request.POST['w2']

        war_participents = (w1, w2)

        fights = int(request.POST['fights'])
        res = []
        ress = []
        while fights > 0:
            while w1.health > 0 and w2.health > 0:
                attacker = random.choice(war_participents)
                defender = w1 if attacker is w2 else w2
                attacker.attack(defender)
            winner = w1.name if w2.health is 0 else w2.name

            res.append(winner)
            w1.health, w2.health = 100, 100
            fights = fights - 1
        ress.append(w1.name + ': ' + str(res.count(w1.name)))
        ress.append(w2.name + ': ' + str(res.count(w2.name)))
        war_winner = w1.name if res.count(w1.name) > res.count(w2.name) else w2.name

        return render(request, 'result.html', {
            'winner': war_winner,
            'process': ress,
        })
    else:
        return render(request, 'war.html')