import numpy as np
import matplotlib.pyplot as plt

from src.PCA_2D import return_two_components_transformed


# Human interact clustering interface class
class HumanClusteringInterface:

    # Initialize, if the size of dataset is larger than sample input, sampling process will be called.
    def __init__(self, in_data, sample=50000):
        if len(in_data.columns) == 2:
            self.self_two_dim_data = in_data
        else:
            self.self_two_dim_data = return_two_components_transformed(in_data)

        self.cluster_list = [0]
        if self.self_two_dim_data.shape[0] > sample:
            self.self_sample_two_dim_data = self.self_two_dim_data.sample(n=sample)
        else:
            self.self_sample_two_dim_data = self.self_two_dim_data

        self.result_df = self.self_two_dim_data

        # Call the interface
        self.clustering_interface()

    def clustering_interface(self):  # Data should be [[x0,y0],[x1,y1],...]
        fig = plt.figure()
        ax_plot = fig.add_subplot(111)
        ax_draw = fig.add_subplot(111)
        ax_draw.patch.set_alpha(0)

        # Draw the data plot
        ax_plot.scatter(np.array(self.self_sample_two_dim_data)[:, 0], np.array(self.self_sample_two_dim_data)[:, 1])

        ax_draw.set_xlim(ax_plot.get_xlim())
        ax_draw.set_ylim(ax_plot.get_ylim())

        current_click = []

        clusters = []

        # Test function for the data point is in the cluster polygon or not.
        def isPointIn(in_testPoint, in_polygon):
            n_polyLines = len(in_polygon)
            result = False

            point_from = in_polygon[0]

            for i_point in range(1, n_polyLines):
                point_to = in_polygon[i_point % n_polyLines]
                if min(point_from[0], point_to[0]) <= in_testPoint[0]:
                    if in_testPoint[0] <= max(point_from[0], point_to[0]):
                        if point_from[0] != point_to[0]:
                            pointLineIntersection = (in_testPoint[0] - point_from[0])
                            pointLineIntersection *= (point_to[1] - point_from[1]) / (point_to[0] - point_from[0])
                            pointLineIntersection += point_from[1]
                            if in_testPoint[1] <= pointLineIntersection:
                                result = not result
                        else:
                            result = not result
                point_from = point_to
            return result

        # make index of the clusters.
        def isThisPointInCluster(in_point, in_draw_list):
            group_index = 0
            for group in in_draw_list:
                if isPointIn(in_point, group):
                    return group_index
                group_index += 1

            return -1

        # return the clustered data
        def clusteringByHumanDraw(in_data, in_draw_list):
            clusterIndexForData_list = []
            data_list = in_data.values.tolist()
            for data in data_list:
                clusterIndexForData_list.append(isThisPointInCluster(data, in_draw_list))

            return clusterIndexForData_list

        # Click event
        def onclick(event):
            current_click.append([event.xdata, event.ydata])
            ax_draw.clear()
            for cluster_points in clusters:
                ax_draw.plot(np.array(cluster_points)[:, 0], np.array(cluster_points)[:, 1], color='g')

            ax_draw.plot(np.array(current_click)[:, 0], np.array(current_click)[:, 1], color='r')

            ax_draw.set_xlim(ax_plot.get_xlim())
            ax_draw.set_ylim(ax_plot.get_ylim())
            ax_draw.patch.set_alpha(0)

            fig.canvas.draw()

        def draw_points(event):
            # Connect with the First Clicked Point
            if event.key == 'z':
                ax_draw.clear()

                current_click.append([current_click[0][0], current_click[0][1]])
                ax_draw.plot(np.array(current_click[:])[:, 0], np.array(current_click[:])[:, 1], color='r')

                clusters.append(current_click[:])
                current_click.clear()

                for cluster_points in clusters:
                    ax_draw.plot(np.array(cluster_points)[:, 0], np.array(cluster_points)[:, 1], color='g')

                ax_draw.set_xlim(ax_plot.get_xlim())
                ax_draw.set_ylim(ax_plot.get_ylim())
                ax_draw.patch.set_alpha(0)

                fig.canvas.draw()

            # Remove the last clicked Point
            if event.key == 'c':

                ax_draw.clear()

                current_click.pop()
                ax_draw.plot(np.array(current_click[:])[:, 0], np.array(current_click[:])[:, 1], color='r')

                for cluster_points in clusters:
                    ax_draw.plot(np.array(cluster_points)[:, 0], np.array(cluster_points)[:, 1], color='g')

                ax_draw.set_xlim(ax_plot.get_xlim())
                ax_draw.set_ylim(ax_plot.get_ylim())
                ax_draw.patch.set_alpha(0)

                fig.canvas.draw()

            # Finish
            if event.key == 'f':

                ax_draw.clear()
                for cluster_points in clusters:
                    ax_draw.plot(np.array(cluster_points)[:, 0], np.array(cluster_points)[:, 1], color='g')

                fig.set_facecolor('tab:gray')
                fig.text(0.5, 0.5, 'Clusterizing Finished', fontsize=30, horizontalalignment='center',
                         verticalalignment='center')

                ax_draw.set_xlim(ax_plot.get_xlim())
                ax_draw.set_ylim(ax_plot.get_ylim())
                ax_draw.patch.set_alpha(0)

                ax_draw.set_facecolor('tab:gray')
                ax_plot.set_facecolor('tab:gray')

                fig.canvas.draw()
                fig.canvas.mpl_disconnect(cid_click)
                fig.canvas.mpl_disconnect(cid_keyboard)

                self.cluster_list[0] = clusteringByHumanDraw(self.self_two_dim_data, clusters)
                self.result_df['cluster'] = self.cluster_list[0]

                # self.result[0] = clusters

        cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
        cid_keyboard = fig.canvas.mpl_connect('key_press_event', draw_points)

    # draw a scatter plot for the result
    def clustering_result(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.scatter(np.array(self.result_df)[:, 0], np.array(self.result_df)[:, 1],
                   c=np.array(self.result_df)[:, 2], cmap="viridis")
