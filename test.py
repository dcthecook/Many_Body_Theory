# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 10:55:03 2023

@author: Enea
"""

import engine.fermions as ef
import engine.bosons as eb
import matplotlib.pyplot as plt

test_object1 = ef.XXX(1, 0.3, 8)
test_object2 = ef.Fermi_Hubbard(5, 10, 1, -0.18)
test_object3 = eb.Bose_Hubbard(5, 6, -1, 0.12, 0.08)

plt.style.use('dark_background')
plt.figure(figsize=(16, 16))

# Plot the first object
plt.subplot(311)  # 1 row, 3 columns, plot 1
plt.imshow(test_object1, cmap='terrain')
plt.title('XXX Model')

# Plot the second object
plt.subplot(312)  # 1 row, 3 columns, plot 2
plt.imshow(test_object2, cmap='terrain')
plt.title('Fermi Hubbard')

# Plot the third object
plt.subplot(313)  # 1 row, 3 columns, plot 3
plt.imshow(test_object3, cmap='terrain')
plt.title('Bose Hubbard')

plt.tight_layout()  # Ensure the subplots are nicely arranged
plt.show()
