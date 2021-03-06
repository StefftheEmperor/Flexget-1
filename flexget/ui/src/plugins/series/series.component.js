/* global angular */
(function () {
    'use strict';

    angular
        .module('plugins.series')
        .component('seriesView', {
            templateUrl: 'plugins/series/series.tmpl.html',
            controllerAs: 'vm',
            controller: seriesController
        });

    function seriesController($mdMedia, $mdDialog, $sce, $timeout, seriesService) {
        var vm = this;

        var options = {
            page: 1,
            'page_size': 10,
            'in_config': 'all',
            'sort_by': 'show_name',
            'descending': false
        };

        var params = {
            forget: true
        };

        vm.searchTerm = '';

        vm.$onInit = activate;
        vm.forgetShow = forgetShow;
        vm.search = search;
        vm.toggleEpisodes = toggleEpisodes;
        vm.areEpisodesOnShowRow = areEpisodesOnShowRow;

        function activate() {
            getSeriesList();
        }

        function getSeriesList() {
            seriesService.getShows(options).then(function (data) {
                vm.series = data.shows;

                vm.currentPage = data.page;
                vm.totalShows = data['total_number_of_shows'];
                vm.pageSize = data['page_size'];
            });
        }

        function forgetShow(show) {
            var confirm = $mdDialog.confirm()
                .title('Confirm forgetting show.')
                .htmlContent($sce.trustAsHtml('Are you sure you want to completely forget <b>' + show['show_name'] + '</b>?<br /> This will also forget all downloaded releases.'))
                .ok('Forget')
                .cancel('No');

            $mdDialog.show(confirm).then(function () {
                seriesService.deleteShow(show, params).then(function () {
                    getSeriesList();
                });
            });
        }

        //Call from the pagination to update the page to the selected page
        vm.updateListPage = function (index) {
            options.page = index;

            getSeriesList();
        };


        function search() {
            vm.searchTerm ? searchShows() : emptySearch();

            function searchShows() {
                seriesService.searchShows(vm.searchTerm).then(function (data) {
                    vm.series = data.shows;
                });
            }

            function emptySearch() {
                options.page = 1;
                getSeriesList();
            }
        }

        function toggleEpisodes(show) {
            show === vm.selectedShow ? clearShow() : setSelectedShow();

            function clearShow() {
                vm.selectedShow = null;
            }

            function setSelectedShow() {
                vm.selectedShow = null;
                $timeout(function () {
                    vm.selectedShow = show;
                });
            }
        }

        function getNumberOfColumns() {
            if ($mdMedia('gt-lg')) {
                return 3;
            } else if ($mdMedia('gt-md')) {
                return 2;
            }
            return 1;
        }

        function areEpisodesOnShowRow(index) {
            var show = vm.selectedShow;

            if (!show) {
                return false;
            }
            
            var numberOfColumns = getNumberOfColumns();

            var column = index % numberOfColumns;
            var row = (index - column) / numberOfColumns;

            var showIndex = vm.series.indexOf(show);
            var showColumn = showIndex % numberOfColumns;
            var showRow = (showIndex - showColumn) / numberOfColumns;

            if (row !== showRow) {
                return false;
            }

            //Check if not last series, since it doesn't work correctly with the matrix here
            if (index !== vm.series.length - 1 && column !== numberOfColumns - 1) {
                return false;
            }

            return true;
        }
    }
}());
