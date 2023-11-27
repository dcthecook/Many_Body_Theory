# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 10:55:03 2023

@author: Enea
"""

import engine.fermions as ef
import engine.bosons as eb
import matplotlib.pyplot as plt

hopping_term = -1
potential = -0.2
chem = 0.03
test_object1 = ef.XXX_Z(-1, 0.3, 8)
test_object2 = ef.Fermi_Hubbard(5, 10, hopping_term, potential, chem, 'nospin')
test_object3 = ef.Fermi_Hubbard(5, 5, hopping_term, potential, chem, 'spin')
test_object4 = eb.Bose_Hubbard(5, 6, -1, 0.12, 0.08)

plt.style.use('dark_background')
plt.figure(figsize=(100, 100))
font = 50
# Plot the first object
plt.subplot(411)  # 1 row, 3 columns, plot 1
plt.imshow(test_object1, cmap='ocean')
plt.title('XXX Model with Z interaction, 8 spin sites', fontsize=font)

# Plot the second object
plt.subplot(412)  # 1 row, 3 columns, plot 2
plt.imshow(test_object2, cmap='ocean')
plt.title('Spinless Fermi Hubbard, 5 fermions on 10 sites', fontsize=font )

# Plot the third object
plt.subplot(413)  # 1 row, 3 columns, plot 3
plt.imshow(test_object3, cmap='ocean')
plt.title('Spin Fermi Hubbard, 5 fermions on 5 sites', fontsize=font)

# Plot the fourth object
plt.subplot(414)  # 1 row, 3 columns, plot 3
plt.imshow(test_object4, cmap='ocean')
plt.title('Bose Hubbard, 5 bosons on 6 sites', fontsize=font)

plt.tight_layout()  # Ensure the subplots are nicely arranged
plt.show()